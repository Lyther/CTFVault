SHELL := /bin/bash
.DEFAULT_GOAL := help
.ONESHELL:

# Usage:
#   make event NAME="DEF CON Quals 2026" [STYLE=numbered|categorized]
#   make chall EVENT="CPCTF 2026" NAME="cool-pwn" [CATEGORY=Pwn] [ID=42]
#   make lint
#   make stats
#   make clean

NAME      ?=
EVENT     ?=
CATEGORY  ?=
ID        ?=
STYLE     ?= numbered

.PHONY: help
help:
	@echo "Targets:"
	@echo "  event   NAME=\"...\" [STYLE=numbered|categorized]"
	@echo "  chall   EVENT=\"...\" NAME=\"...\" [CATEGORY=...] [ID=NN]"
	@echo "  lint    markdownlint + shellcheck"
	@echo "  stats   count challenge dirs (DESCRIPTION.md|challenge.md|challenge.json) + writeups (any case)"
	@echo "  tree    show event/challenge tree"
	@echo "  clean   remove .DS_Store, __pycache__, *.pyc"

.PHONY: event
event:
	@test -n "$(NAME)" || { echo "ERROR: NAME=\"...\" required"; exit 2; }
	@./scripts/new-event.sh "$(NAME)" "$(STYLE)"

.PHONY: chall
chall:
	@test -n "$(EVENT)" || { echo "ERROR: EVENT=\"...\" required"; exit 2; }
	@test -n "$(NAME)"  || { echo "ERROR: NAME=\"...\" required";  exit 2; }
	@./scripts/new-challenge.sh "$(EVENT)" "$(NAME)" "$(CATEGORY)" "$(ID)"

.PHONY: lint
lint:
	@command -v markdownlint >/dev/null 2>&1 && markdownlint '**/*.md' --ignore node_modules --ignore '*/node_modules/**' || echo "skip: markdownlint not installed (npm i -g markdownlint-cli)"
	@command -v shellcheck   >/dev/null 2>&1 && shellcheck scripts/*.sh || echo "skip: shellcheck not installed (brew install shellcheck)"

.PHONY: stats
stats:
	@./scripts/stats.sh

.PHONY: tree
tree:
	@command -v tree >/dev/null 2>&1 || { echo "install tree: brew install tree"; exit 1; }
	@tree -L 3 -I 'node_modules|__pycache__|.venv|venv|target|dist|build|.cursor|.git'

.PHONY: clean
clean:
	@find . -name '.DS_Store' -delete
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
	@echo "cleaned: .DS_Store, __pycache__, *.pyc"
