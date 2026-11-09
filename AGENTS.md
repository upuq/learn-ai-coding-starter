# AGENTS.md

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang. For language behavior, syntax, operators, and grammar, see [docs/spec.md](docs/spec.md) — treat it as the source of truth.

## Project layout

- `sloperator.py` — CLI entrypoint (`--check` parses without running).
- `sloperator/lexer/` → `sloperator/parser/` (AST in `ast.py`) → `sloperator/evaluator/` — tokenize, parse, interpret.
- `sloperator/runner.py` — `run_source()` and `check_program()`, used by tests; returns stdout, stderr, and an exit code.
- `examples/` — runnable `.slop` programs; every file is exercised by `tests/test_examples.py`.
- `tests/` — pytest suite. `playground/` — local web runner.
- `sloperator/parser/AGENTS.md` — parser-specific conventions.

## Validation

Run all four from the repo root:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

After any code change, run the formatter before the checks above:

```bash
uv run ruff format
```

For comparison tests, run just that file:

```bash
uv run pytest tests/test_comparisons.py
```

## Regression tests

Add a regression test when you:

- fix a bug — reproduce the failure first, then assert the corrected behavior;
- add or change a language feature, operator precedence, or parse rule;
- change an error message, exit code, or CLI flag.

Prefer asserting observable behavior through `run_source()` or the CLI (stdout, stderr, exit code). For lexer/parser bugs, assert the token or AST result directly when that is the contract being fixed.
