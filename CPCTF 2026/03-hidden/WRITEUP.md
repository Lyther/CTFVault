# Hidden

**Idea:** Linux x86-64 ELF; the flag lives in read-only data and shows up in plain `strings`.

**Solve:** `strings hidden | grep CPCTF` (or search `.rodata` in a disassembler).

**Note:** Binary targets Linux/glibc; on macOS, static analysis / `strings` is enough.

**Flag:** `CPCTF{H1dd3n_1n_5tr1ngs}`
