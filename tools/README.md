# tools

Reusable scripts and helpers across challenges.

## Conventions

- One tool = one file (or one self-contained subfolder).
- Python scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata so they run with `uv run script.py` without a project venv:

  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = ["pwntools", "scapy"]
  # ///
  ```

- Shell scripts: `#!/usr/bin/env bash` + `set -euo pipefail` + `shellcheck` clean.
- Each tool: 5-line header explaining what it does and one usage example. No more.

## Promote pattern

If the same code appears in 3+ `solve.py` files across challenges, extract it here.
