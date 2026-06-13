#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pefile",
#   "unicorn",
# ]
# ///

import pathlib
import re
import struct

import pefile
from unicorn import (
    UC_ARCH_X86,
    UC_HOOK_CODE,
    UC_HOOK_MEM_INVALID,
    UC_MODE_64,
    Uc,
)
from unicorn.x86_const import (
    UC_X86_REG_FS_BASE,
    UC_X86_REG_GS_BASE,
    UC_X86_REG_R8,
    UC_X86_REG_R9,
    UC_X86_REG_R10,
    UC_X86_REG_R11,
    UC_X86_REG_R12,
    UC_X86_REG_R13,
    UC_X86_REG_R14,
    UC_X86_REG_R15,
    UC_X86_REG_RAX,
    UC_X86_REG_RBP,
    UC_X86_REG_RBX,
    UC_X86_REG_RCX,
    UC_X86_REG_RDI,
    UC_X86_REG_RDX,
    UC_X86_REG_RIP,
    UC_X86_REG_RSI,
    UC_X86_REG_RSP,
)

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "coinjam.exe"

BASE = 0x140000000
API_BASE = 0x180000000
STACK_BASE = 0x70000000
STACK_SIZE = 0x200000
TEB_BASE = 0x60000000
TEB_SIZE = 0x2000
HEAP_BASE = 0x51000000
HEAP_SIZE = 0x400000
BUFFER_BASE = 0x50000000
BUFFER_SIZE = 0x2000
FAKE_HEAP_HANDLE = 0x90000000
SENTINEL = 0x13370000
PAGE = 0x1000

STARTUP_B64_RVA = 0x11AA0
STARTUP_B64_LEN = 0x754

COOKIE_INIT = 0x140004258
UPDATE_FUNC = 0x140002560

PLAYER_X = 0x14001D000
PLAYER_Y = 0x14001D004
PLAYER_VX = 0x14001D008
PLAYER_VY = 0x14001D00C
COIN_COUNT = 0x14001D01C
COIN_MASK = 0x14001D020
COIN_COUNTER2 = 0x14001D024
FRAME_COUNTER = 0x14001D028
INPUT_FLAGS = 0x14001D02C
SEED = 0x14001D038
HWND_SLOT = 0x14001DBD0
STARTUP_BUF_PTR = 0x14001DBD8
STARTUP_BUF_LEN = 0x14001DBE8
STARTUP_BUF_CAP = 0x14001DBF0

QPC_VALUE = 0x1122334455667788
SEED_VALUE = 0x1E538725


def align_up(value: int, align: int = PAGE) -> int:
    return (value + align - 1) & ~(align - 1)


def pack_u32(value: int) -> bytes:
    return struct.pack("<I", value & 0xFFFFFFFF)


def pack_u64(value: int) -> bytes:
    return struct.pack("<Q", value & 0xFFFFFFFFFFFFFFFF)


def pack_f32(value: float) -> bytes:
    return struct.pack("<f", value)


def unpack_u64(data: bytes) -> int:
    return struct.unpack("<Q", data)[0]


class Emulator:
    def __init__(self, path: pathlib.Path) -> None:
        self.pe = pefile.PE(str(path))
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.api_names: dict[int, str] = {}
        self.heap_next = HEAP_BASE
        self.heap_allocs: dict[int, int] = {}
        self.last_error = 0
        self.fls: dict[int, int] = {}
        self.stop_reason: str | None = None
        self.messages: list[tuple[str, str]] = []
        self._map_image()
        self._map_stack()
        self._map_heap()
        self._map_teb_peb()
        self._map_sentinel()
        self._patch_imports()
        self.uc.hook_add(UC_HOOK_CODE, self._hook_code)
        self.uc.hook_add(UC_HOOK_MEM_INVALID, self._hook_invalid)

    def _map_image(self) -> None:
        mapped = self.pe.get_memory_mapped_image()
        size = align_up(max(len(mapped), self.pe.OPTIONAL_HEADER.SizeOfImage))
        self.uc.mem_map(BASE, size)
        self.uc.mem_write(BASE, mapped)

    def _map_stack(self) -> None:
        self.uc.mem_map(STACK_BASE, STACK_SIZE)

    def _map_heap(self) -> None:
        self.uc.mem_map(HEAP_BASE, HEAP_SIZE)
        self.uc.mem_map(BUFFER_BASE, BUFFER_SIZE)

    def _map_teb_peb(self) -> None:
        self.uc.mem_map(TEB_BASE, TEB_SIZE)
        peb = TEB_BASE + 0x1000
        self.uc.mem_write(TEB_BASE + 0x60, pack_u64(peb))
        self.uc.reg_write(UC_X86_REG_GS_BASE, TEB_BASE)
        self.uc.reg_write(UC_X86_REG_FS_BASE, TEB_BASE)

    def _map_sentinel(self) -> None:
        self.uc.mem_map(SENTINEL & ~0xFFF, PAGE)
        self.uc.mem_write(SENTINEL, b"\xc3")

    def _patch_imports(self) -> None:
        self.uc.mem_map(API_BASE, PAGE)
        stub = API_BASE
        for entry in self.pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                name = imp.name.decode() if imp.name else f"ord_{imp.ordinal}"
                self.uc.mem_write(imp.address, pack_u64(stub))
                self.api_names[stub] = name
                self.uc.mem_write(stub, b"\xc3")
                stub += 0x10

    def _hook_invalid(self, uc, access, address, size, value, _user_data):
        self.stop_reason = (
            f"invalid_mem access={access} addr={hex(address)} "
            f"size={size} rip={hex(uc.reg_read(UC_X86_REG_RIP))}"
        )
        return False

    def _api_return(self, value: int = 0) -> None:
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        ret = unpack_u64(bytes(self.uc.mem_read(rsp, 8)))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        self.uc.reg_write(UC_X86_REG_RAX, value)
        self.uc.reg_write(UC_X86_REG_RIP, ret)

    def _heap_alloc(self, size: int) -> int:
        size = align_up(max(size, 0x10), 0x10)
        addr = self.heap_next
        end = addr + size
        if end > HEAP_BASE + HEAP_SIZE:
            raise RuntimeError(f"fake heap exhausted while allocating {hex(size)}")
        self.heap_next = end
        self.heap_allocs[addr] = size
        self.uc.mem_write(addr, b"\x00" * size)
        return addr

    def _read_cstring(self, addr: int, limit: int = 0x400) -> str:
        out = bytearray()
        for _ in range(limit):
            byte = bytes(self.uc.mem_read(addr, 1))
            if byte == b"\x00":
                break
            out += byte
            addr += 1
        return out.decode("utf-8", errors="replace")

    def _hook_code(self, uc, address, _size, _user_data) -> None:
        if address == SENTINEL:
            self.stop_reason = "returned"
            uc.emu_stop()
            return
        name = self.api_names.get(address)
        if name is None:
            return
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        r9 = uc.reg_read(UC_X86_REG_R9)
        if name == "GetSystemTimeAsFileTime":
            uc.mem_write(rcx, pack_u64(0x01DABCD123456789))
            self._api_return(0)
            return
        if name == "GetCurrentThreadId":
            self._api_return(0x1234)
            return
        if name == "GetCurrentProcessId":
            self._api_return(0x5678)
            return
        if name == "QueryPerformanceCounter":
            uc.mem_write(rcx, pack_u64(QPC_VALUE))
            self._api_return(1)
            return
        if name == "GetCurrentProcess":
            self._api_return(0xFFFFFFFFFFFFFFFF)
            return
        if name == "GetProcessHeap":
            self._api_return(FAKE_HEAP_HANDLE)
            return
        if name == "GetAsyncKeyState":
            self._api_return(0)
            return
        if name == "HeapAlloc":
            self._api_return(self._heap_alloc(r8))
            return
        if name == "HeapReAlloc":
            old_ptr = r9
            new_ptr = self._heap_alloc(r8)
            old_size = self.heap_allocs.get(old_ptr, 0)
            if old_size:
                chunk = bytes(uc.mem_read(old_ptr, min(old_size, r8)))
                uc.mem_write(new_ptr, chunk)
            self._api_return(new_ptr)
            return
        if name == "HeapSize":
            self._api_return(self.heap_allocs.get(r8, 0xFFFFFFFFFFFFFFFF))
            return
        if name == "GetLastError":
            self._api_return(self.last_error)
            return
        if name == "SetLastError":
            self.last_error = rcx & 0xFFFFFFFF
            self._api_return(0)
            return
        if name == "FlsSetValue":
            self.fls[rcx] = rdx
            self._api_return(1)
            return
        if name == "FlsGetValue":
            self._api_return(self.fls.get(rcx, 0))
            return
        if name in {
            "EnterCriticalSection",
            "LeaveCriticalSection",
            "InitializeCriticalSection",
            "DeleteCriticalSection",
        }:
            self._api_return(0)
            return
        if name in {
            "InitializeCriticalSectionAndSpinCount",
            "InitializeCriticalSectionEx",
        }:
            self._api_return(1)
            return
        if name == "MessageBoxA":
            text = self._read_cstring(rdx) if rdx else ""
            title = self._read_cstring(r8) if r8 else ""
            self.messages.append((title, text))
            self._api_return(1)
            return
        self._api_return(0)

    def run_func(self, addr: int, count: int) -> None:
        rsp = STACK_BASE + STACK_SIZE - 0x1000
        rsp &= ~0xF
        rsp -= 8
        self.uc.mem_write(rsp, pack_u64(SENTINEL))
        self.uc.reg_write(UC_X86_REG_RSP, rsp)
        for reg in (
            UC_X86_REG_RAX,
            UC_X86_REG_RBX,
            UC_X86_REG_RCX,
            UC_X86_REG_RDX,
            UC_X86_REG_RSI,
            UC_X86_REG_RDI,
            UC_X86_REG_R8,
            UC_X86_REG_R9,
            UC_X86_REG_R10,
            UC_X86_REG_R11,
            UC_X86_REG_R12,
            UC_X86_REG_R13,
            UC_X86_REG_R14,
            UC_X86_REG_R15,
            UC_X86_REG_RBP,
        ):
            self.uc.reg_write(reg, 0)
        self.stop_reason = None
        self.uc.reg_write(UC_X86_REG_RIP, addr)
        self.uc.emu_start(addr, SENTINEL, count=count)

    def seed_startup_buffer(self) -> None:
        source = BASE + STARTUP_B64_RVA
        blob = bytes(self.uc.mem_read(source, STARTUP_B64_LEN)) + b"\x00"
        self.uc.mem_write(BUFFER_BASE, blob)
        self.uc.mem_write(STARTUP_BUF_PTR, pack_u64(BUFFER_BASE))
        self.uc.mem_write(STARTUP_BUF_LEN, pack_u64(STARTUP_B64_LEN))
        self.uc.mem_write(STARTUP_BUF_CAP, pack_u64(0x75F))

    def seed_game_state(self) -> None:
        self.seed_startup_buffer()
        self.uc.mem_write(COIN_COUNT, pack_u32(10))
        self.uc.mem_write(COIN_MASK, pack_u32(0x7F))
        self.uc.mem_write(COIN_COUNTER2, pack_u32(7))
        self.uc.mem_write(FRAME_COUNTER, pack_u32(1234))
        self.uc.mem_write(SEED, pack_u32(SEED_VALUE))
        self.uc.mem_write(HWND_SLOT, pack_u64(1))
        self.uc.mem_write(PLAYER_X, pack_f32(880.0))
        self.uc.mem_write(PLAYER_Y, pack_f32(400.0))
        self.uc.mem_write(PLAYER_VX, pack_f32(0.0))
        self.uc.mem_write(PLAYER_VY, pack_f32(0.0))
        self.uc.mem_write(INPUT_FLAGS, b"\x00" * 6)

    def recover_flag(self) -> str:
        heap_size = self.heap_next - HEAP_BASE
        if heap_size <= 0:
            raise RuntimeError("protected path never allocated heap memory")
        blob = bytes(self.uc.mem_read(HEAP_BASE, heap_size))
        match = re.search(rb"CIT\{[^}]+\}", blob)
        if not match:
            raise RuntimeError("no flag-shaped string found in emulated heap")
        return match.group().decode()


def main() -> None:
    emu = Emulator(CHALLENGE)
    emu.run_func(COOKIE_INIT, count=20_000)
    emu.seed_game_state()
    emu.run_func(UPDATE_FUNC, count=200_000_000)
    flag = emu.recover_flag()
    print(flag)


if __name__ == "__main__":
    main()
