# Hello LaTeX3

The full missing expl3 function is:

```text
\seq_set_from_clist:Nn
```

Why this one:

```tex
\seq_new:N \l_my_char_code_seq
\tl_new:N  \l_my_result_tl

\cs_new_protected:Npn \my_convert_clist_to_string:n #1
  {
    \???:Nn \l_my_char_code_seq { #1 }
    \tl_clear:N \l_my_result_tl
    \seq_map_inline:Nn \l_my_char_code_seq
      {
        \tl_put_right:Nx \l_my_result_tl { \char_generate:nn { ##1 } { 12 } }
      }
    \tl_use:N \l_my_result_tl
  }
```

`#1` is a comma list of character codes, and the next line immediately iterates over `\l_my_char_code_seq` using `\seq_map_inline:Nn`.

So the missing function must:

1. take a sequence variable as its first argument,
2. take normal input as its second argument,
3. interpret that input as a comma list,
4. store the result into the sequence.

That is exactly what `\seq_set_from_clist:Nn` does.

However, the challenge asks for the string that replaces only `???` in

```tex
\???:Nn
```

So the required answer is not the full function name with its argument signature. The `:Nn` part is already present in the source.

The missing basename is:

```text
seq_set_from_clist
```

So the flag is:

```text
CPCTF{seq_set_from_clist}
```
