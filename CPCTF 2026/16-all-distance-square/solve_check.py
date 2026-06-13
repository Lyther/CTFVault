#!/usr/bin/env python3
import time

MAX_SUM = 200 * 200
SQUARES = {k * k for k in range(int(MAX_SUM**0.5) + 2)}


def make_adj(es, N):
    adj = {i: [] for i in range(1, N + 1)}
    for u, v, w, eid in es:
        adj[u].append((v, w, eid))
        adj[v].append((u, w, eid))
    return adj


def pair_has_square(adj, i, j):
    if i > j:
        i, j = j, i
    ok = [False]

    def dfs(u, target, vis, sm):
        if ok[0]:
            return
        if u == target:
            if sm in SQUARES:
                ok[0] = True
            return
        for v, w, eid in adj[u]:
            if v in vis:
                continue
            dfs(v, target, vis | {v}, sm + w)

    dfs(i, j, frozenset({i}), 0)
    return ok[0]


def new_vertex_ok(adj, nv):
    for i in range(1, nv):
        if not pair_has_square(adj, i, nv):
            return False
    return True


def solve(N):
    if N == 2:
        return [(1, 2, 1, 1)]
    edges = [(1, 2, 16, 1), (2, 3, 9, 2), (1, 3, 25, 3)]
    used = {16, 9, 25}
    eid = 3
    pairs = [(1, 2), (1, 3), (2, 3)]

    def rec(nv):
        nonlocal edges, used, eid
        if nv == N + 1:
            return True
        avail = [x for x in range(1, 201) if x not in used]
        for uu, vv in pairs:
            for a in avail:
                for b in avail:
                    if a == b:
                        continue
                    ne = list(edges) + [(uu, nv, a, eid + 1), (vv, nv, b, eid + 2)]
                    adj = make_adj(ne, nv)
                    if not new_vertex_ok(adj, nv):
                        continue
                    olde, oldu, oldeid = edges, used.copy(), eid
                    edges = ne
                    used.add(a)
                    used.add(b)
                    eid += 2
                    if rec(nv + 1):
                        return True
                    edges, used, eid = olde, oldu, oldeid
        return False

    return edges if rec(4) else None


if __name__ == "__main__":
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    t0 = time.time()
    e = solve(n)
    print(
        n, "OK" if e else "FAIL", round(time.time() - t0, 2), "M", len(e) if e else None
    )
