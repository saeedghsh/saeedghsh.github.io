VENV ?= .venv
PYTHON ?= python3
PORT ?= 8001
MARKDOWN_FILES = docs/*.md README.md

.PHONY: create-env serve build format check

create-env:
	$(PYTHON) -m venv "$(VENV)"
	"$(VENV)/bin/python" -m pip install -r requirements.txt

serve:
	"$(VENV)/bin/zensical" serve --dev-addr 127.0.0.1:$(PORT)

build:
	"$(VENV)/bin/zensical" build --strict

format:
	"$(VENV)/bin/mdformat" $(MARKDOWN_FILES)

check:
	"$(VENV)/bin/mdformat" --check $(MARKDOWN_FILES)
	"$(VENV)/bin/rumdl" check --disable MD013 $(MARKDOWN_FILES)
	"$(VENV)/bin/yamllint" .yamllint.yml .github/workflows/site.yml
	$(MAKE) build
	"$(VENV)/bin/python" scripts/check_site.py
