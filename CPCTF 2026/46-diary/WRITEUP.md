# diary

Flag:

```text
CPCTF{s7r0ng1y_r3c0mmend3d_t0_u3e_3m4r7_p01nt3r}
```

The core bug is an accidental shallow copy. `Diary` owns a raw `DiaryImpl *impl`, but it does not define a copy constructor:

```cpp
class Diary {
public:
    Diary(const std::string &content, int month = 0, int day = 0) {
        impl = new DiaryImpl(content, month, day);
    }

    ~Diary() { delete impl; }
    ...
private:
    DiaryImpl *impl;
};
```

and `show_with_emphasis` takes `Diary` by value:

```cpp
void show_with_emphasis(Diary diary) {
    diary.to_upper();
    diary.show();
}
```

So `show_with_emphasis(diaries[index])` copies only the pointer, then the temporary destructor frees the original `DiaryImpl`. The `diaries[index]` entry is left dangling, which gives a use-after-free on a `0x40` heap chunk.

That dangling object is enough for tcache poisoning. `DiaryImpl::set_date` writes the first 8 bytes of the freed chunk:

```cpp
void set_date(int m, int d) {
    month = m;
    day = d;
}
```

After freeing three small diaries with the emphasis function, the first two summaries leak safe-linked tcache pointers. Because those chunks are on the same page, `chunk >> 12` is shared, so the first real `DiaryImpl` address can be recovered exactly. From there, two fixed local offsets matter:

- the reserved `std::vector<Diary>` storage is at `first_impl - 0x22b0`
- the later `getline` buffer used for the fake object is at `first_impl + 0x2c0`

Poisoning the third freed chunk with `vector_base ^ heap_key` makes the next `new DiaryImpl` return the vector storage itself. Creating one filler diary and then one steering diary gives this useful state:

- slot `0` in the vector becomes `fake_addr`, so diary `0` now points to a fake `DiaryImpl`
- diary `4` points back to the vector storage, so updating diary `4` rewrites slot `0`

The fake `DiaryImpl` is placed in the leaked `getline` buffer. Its fake `std::string` points at `.got.plt`, which turns `show(0)` into an arbitrary read. The important detail is to leak `getline@got`, not `strlen@got`: `strlen` is an IFUNC symbol, so its GOT entry points to an optimized resolver target and does not give the libc base directly.

With the leaked `getline` address:

```text
libc = getline@libc - 0x5f7b0
system = libc + 0x58750
```

the final write is:

1. use diary `4` to repoint diary `0` at `strlen@got`
2. use diary `0` to overwrite `strlen@got` with `system`

After that, any later `std::string(line)` construction calls `system(line)` because it internally uses `strlen`. Triggering `update(4, ..., "cat /home/user/flag.txt")` executes the shell command during input parsing and prints the flag.

`solve.py` automates the full chain against the remote service.
