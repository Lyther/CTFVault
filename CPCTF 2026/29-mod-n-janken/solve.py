#!/usr/bin/env python3
"""Solver for mod N Janken (CPCTF 2026 #29).

Idea: xorshift64 is linear over GF(2) with matrix M.  NPC contribution to
column j is M^j * T where T = XOR of NPC seeds (unknown 64-bit constant).
clash = M_S * T XOR K_S where S = active luck columns and K_S = XOR_{j in S} P_j.
Pick S so M_S = 0 (S in the 56-dim kernel of {M^j : 0..119}); clash becomes
fully deterministic = K_S.  Per match, find low-weight S in the kernel coset
of L with K_S mod 101 = player_no.  Use ISD-Prange + Lee-Brickell p=2 to keep
each match within ~30 flips on average.
"""

import argparse
import random
import re
import secrets
import socket
import subprocess
import sys
import time

M64 = (1 << 64) - 1
N_COLS = 120
N_EQS = 64
N_PART = 101
MAX_CHEATS = 600
MATCHES = 20


# ---------- xorshift64 + matrix powers ----------


def xorshift64(n):
    # Match the server bit-for-bit: intermediate XORs are NOT masked, so high
    # bits from `n << 13` leak back into the low 64 via `n >> 7`.
    n ^= n << 13
    n ^= n >> 7
    n ^= n << 17
    return n & M64


def compute_M_powers():
    cols = [1 << i for i in range(64)]  # M^0 = I (column-major)
    powers = [list(cols)]
    for _ in range(N_COLS - 1):
        cols = [xorshift64(c) for c in cols]
        powers.append(list(cols))
    return powers


def matrix_to_int(mat):
    v = 0
    for i, c in enumerate(mat):
        v |= c << (i * 64)
    return v


# ---------- GF(2) linear algebra ----------


def rref_gf2(rows, n_vars):
    rows = list(rows)
    n_rows = len(rows)
    pivots = []
    r = 0
    for c in range(n_vars):
        pivot = -1
        for i in range(r, n_rows):
            if (rows[i] >> c) & 1:
                pivot = i
                break
        if pivot == -1:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(n_rows):
            if i != r and (rows[i] >> c) & 1:
                rows[i] ^= rows[r]
        pivots.append(c)
        r += 1
    return rows[:r], pivots


def kernel_and_parity(vectors, n_vars):
    if not vectors:
        return [], []
    N = max(v.bit_length() for v in vectors)
    rows = []
    for r in range(N):
        row = 0
        for i, v in enumerate(vectors):
            if (v >> r) & 1:
                row |= 1 << i
        if row:
            rows.append(row)
    H, pivots = rref_gf2(rows, n_vars)
    pivot_set = set(pivots)
    free_cols = [c for c in range(n_vars) if c not in pivot_set]
    K_basis = []
    for f in free_cols:
        v = 1 << f
        for i, p in enumerate(pivots):
            if (H[i] >> f) & 1:
                v |= 1 << p
        K_basis.append(v)
    return K_basis, H


# ---------- helpers ----------


def popcount(x):
    return bin(x).count("1")


def syndrome(H, x):
    s = 0
    for i, h in enumerate(H):
        if popcount(h & x) & 1:
            s |= 1 << i
    return s


def K_value(P, y):
    out = 0
    while y:
        lsb = y & -y
        out ^= P[lsb.bit_length() - 1]
        y ^= lsb
    return out


def permute_int(v, inv_perm):
    out = 0
    while v:
        lsb = v & -v
        c = lsb.bit_length() - 1
        out |= 1 << inv_perm[c]
        v ^= lsb
    return out


def build_y(y_basic, y_free, perm, n_eqs):
    y = 0
    tmp = y_basic
    while tmp:
        lsb = tmp & -tmp
        y |= 1 << perm[lsb.bit_length() - 1]
        tmp ^= lsb
    tmp = y_free
    while tmp:
        lsb = tmp & -tmp
        y |= 1 << perm[n_eqs + lsb.bit_length() - 1]
        tmp ^= lsb
    return y


# ---------- ISD-Prange + Lee-Brickell p=2 ----------


def solve_match(
    H,
    s,
    P,
    K_x_L,
    n_target,
    weight_budget=40,
    max_trials=400,
    time_limit=15.0,
):
    n_eqs = N_EQS
    n_cols = N_COLS
    n_free = n_cols - n_eqs

    best_y = None
    best_w = weight_budget + 1

    deadline = time.time() + time_limit
    trials = 0
    while trials < max_trials and time.time() < deadline:
        trials += 1
        perm = list(range(n_cols))
        random.shuffle(perm)
        inv_perm = [0] * n_cols
        for i, p in enumerate(perm):
            inv_perm[p] = i

        H_p = [permute_int(h, inv_perm) for h in H]
        s_p = s

        singular = False
        for c in range(n_eqs):
            pivot = -1
            for i in range(c, n_eqs):
                if (H_p[i] >> c) & 1:
                    pivot = i
                    break
            if pivot == -1:
                singular = True
                break
            if pivot != c:
                H_p[c], H_p[pivot] = H_p[pivot], H_p[c]
                bc = (s_p >> c) & 1
                bp = (s_p >> pivot) & 1
                if bc != bp:
                    s_p ^= (1 << c) | (1 << pivot)
            pivot_row = H_p[c]
            sp_c = (s_p >> c) & 1
            for i in range(n_eqs):
                if i != c and (H_p[i] >> c) & 1:
                    H_p[i] ^= pivot_row
                    if sp_c:
                        s_p ^= 1 << i
        if singular:
            continue

        # H_p is now [I | H'].  Free-column j contributes column D[j] (64-bit) to basic part.
        D = [0] * n_free
        for i in range(n_eqs):
            tmp = H_p[i] >> n_eqs
            while tmp:
                lsb = tmp & -tmp
                D[lsb.bit_length() - 1] |= 1 << i
                tmp ^= lsb

        K_per_basic = [P[perm[i]] for i in range(n_eqs)]
        K_per_free = [P[perm[n_eqs + j]] for j in range(n_free)]

        def K_basic(v):
            out = 0
            while v:
                lsb = v & -v
                out ^= K_per_basic[lsb.bit_length() - 1]
                v ^= lsb
            return out

        K_s = K_basic(s_p)
        K_D = [K_basic(d) for d in D]
        K_off = [K_D[j] ^ K_per_free[j] for j in range(n_free)]

        # p=0 candidate
        w = popcount(s_p)
        if w < best_w and (K_x_L ^ K_s) % 101 == n_target:
            best_y = build_y(s_p, 0, perm, n_eqs)
            best_w = w

        # p=1 candidates
        for j in range(n_free):
            yb = s_p ^ D[j]
            w = popcount(yb) + 1
            if w >= best_w:
                continue
            if (K_x_L ^ K_s ^ K_off[j]) % 101 == n_target:
                best_y = build_y(yb, 1 << j, perm, n_eqs)
                best_w = w

        # p=2 candidates
        if best_w > 2:
            for j in range(n_free):
                yb_j = s_p ^ D[j]
                K_y_j = K_s ^ K_off[j]
                D_k_arr = D
                K_off_arr = K_off
                bw = best_w
                for k in range(j + 1, n_free):
                    yb = yb_j ^ D_k_arr[k]
                    w = popcount(yb) + 2
                    if w >= bw:
                        continue
                    if (K_x_L ^ K_y_j ^ K_off_arr[k]) % 101 == n_target:
                        best_y = build_y(yb, (1 << j) | (1 << k), perm, n_eqs)
                        best_w = w
                        bw = w

        if best_w <= 22:  # plenty good, stop early
            break

    return best_y, best_w, trials


# ---------- I/O abstraction ----------


class Comm:
    def __init__(self):
        self.buf = b""

    def _read_chunk(self):
        raise NotImplementedError

    def recv_until(self, marker):
        markers = [marker] if isinstance(marker, bytes) else list(marker)
        while True:
            for m in markers:
                idx = self.buf.find(m)
                if idx != -1:
                    end = idx + len(m)
                    out = self.buf[:end]
                    self.buf = self.buf[end:]
                    return out
            chunk = self._read_chunk()
            if not chunk:
                out = self.buf
                self.buf = b""
                return out
            self.buf += chunk

    def send_line(self, s):
        if isinstance(s, str):
            s = s.encode()
        self._write(s + b"\n")


class TcpComm(Comm):
    def __init__(self, host, port):
        super().__init__()
        self.sock = socket.create_connection((host, port))

    def _read_chunk(self):
        return self.sock.recv(4096)

    def _write(self, data):
        self.sock.sendall(data)

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


class SubprocComm(Comm):
    def __init__(self, cmd, env=None):
        super().__init__()
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            bufsize=0,
        )

    def _read_chunk(self):
        return self.proc.stdout.read(1024)

    def _write(self, data):
        self.proc.stdin.write(data)
        self.proc.stdin.flush()

    def close(self):
        try:
            self.proc.stdin.close()
        except Exception:
            pass
        self.proc.wait()


# ---------- main ----------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--server", default="server.py")
    ap.add_argument("--host", default="133.88.122.244")
    ap.add_argument("--port", type=int, default=32035)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("[*] Computing kernel of {M^j}...")
    t0 = time.time()
    Ms = compute_M_powers()
    vectors = [matrix_to_int(m) for m in Ms]
    K_basis, H = kernel_and_parity(vectors, N_COLS)
    print(f"    K dim={len(K_basis)}, H rank={len(H)}, t={time.time() - t0:.2f}s")
    assert len(K_basis) == 56 and len(H) == 64

    for k in K_basis:
        for h in H:
            assert popcount(h & k) & 1 == 0
    print("[*] Kernel/parity verified")

    P = [secrets.randbits(64) for _ in range(N_COLS)]

    if args.local:
        import os

        env = dict(os.environ)
        env["FLAG"] = env.get("FLAG", "TEST{ok123}")
        comm = SubprocComm(["python3", args.server], env=env)
    else:
        comm = TcpComm(args.host, args.port)

    print(comm.recv_until(b"Your Strategy: ").decode(errors="ignore"))
    comm.send_line(" ".join(str(p) for p in P))

    cheats_used = 0
    for match in range(MATCHES):
        data = comm.recv_until(b"What will you do?").decode(errors="ignore")
        m_no = re.search(r"Your Number is No: (\d+)", data)
        m_lp = re.search(r"Current Luck Pattern: (\d+)", data)
        if not m_no or not m_lp:
            print("[!] parse failed:", data[-500:])
            return
        player_no = int(m_no.group(1))
        luck_str = m_lp.group(1)
        x_L = 0
        for j, ch in enumerate(luck_str):
            if ch == "1":
                x_L |= 1 << j

        K_x_L = K_value(P, x_L)
        s = syndrome(H, x_L)

        budget_left = MAX_CHEATS - cheats_used
        matches_left = MATCHES - match
        target = max(35, budget_left // matches_left + 8)

        t0 = time.time()
        y, w, trials = solve_match(
            H,
            s,
            P,
            K_x_L,
            player_no,
            weight_budget=target,
            max_trials=600,
            time_limit=20.0,
        )
        dt = time.time() - t0

        if y is None:
            print(f"[!] no solution for match {match + 1}")
            return

        x_S = x_L ^ y
        for h in H:
            assert popcount(h & x_S) & 1 == 0, "x_S not in kernel"
        assert K_value(P, x_S) % 101 == player_no, "K mismatch"

        print(
            f"  match {match + 1:2d}: no={player_no:3d}, flips={w:3d}, "
            f"trials={trials:4d}, t={dt:5.2f}s, total={cheats_used + w}",
        )

        flips = []
        tmp = y
        while tmp:
            lsb = tmp & -tmp
            flips.append(lsb.bit_length() - 1)
            tmp ^= lsb

        for f in flips:
            comm.send_line("C")
            comm.recv_until(b"Which luck index to flip?: ")
            comm.send_line(str(f))
            comm.recv_until(b"What will you do?")
        comm.send_line("G")
        cheats_used += len(flips)

        result = comm.recv_until(
            [
                b"You lost",
                b"What an incredible match!",
                b"TOURNAMENT COMPLETED",
                b"SECURITY",
            ],
        )
        if b"You lost" in result:
            print("[!] LOST:", result.decode(errors="ignore"))
            return
        if b"SECURITY" in result:
            print("[!] CHEAT DETECTED:", result.decode(errors="ignore"))
            return

    # tournament completed; flag follows
    sys.stdout.write(comm.buf.decode(errors="ignore"))
    sys.stdout.flush()
    comm.buf = b""
    if not isinstance(comm, TcpComm):
        try:
            tail = comm.proc.stdout.read()
            sys.stdout.write(tail.decode(errors="ignore"))
        except Exception:
            pass
    else:
        comm.sock.settimeout(5.0)
        try:
            while True:
                chunk = comm.sock.recv(4096)
                if not chunk:
                    break
                sys.stdout.write(chunk.decode(errors="ignore"))
                sys.stdout.flush()
        except TimeoutError:
            pass

    print(f"\n[*] Done. Total cheats used: {cheats_used}/{MAX_CHEATS}")


if __name__ == "__main__":
    main()
