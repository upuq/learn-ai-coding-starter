# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Quick Start

Programs use the `.slop` extension:

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check path/to/program.slop   # syntax only
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.

## Layout

| Path                    | What it is                              |
| ----------------------- | --------------------------------------- |
| `sloperator.py`         | Command-line entrypoint                 |
| `sloperator/lexer/`     | Source text to tokens                   |
| `sloperator/parser/`    | Tokens to AST                           |
| `sloperator/evaluator/` | Values, environments, the interpreter   |
| `sloperator/runner.py`  | Runs source through all three stages    |
| `docs/spec.md`          | The language specification              |
| `examples/`             | Example programs                        |
| `tests/`                | Pytest suite                            |
| `playground/`           | Web server and editor page              |

See [docs/spec.md](docs/spec.md) for the complete language reference, including syntax, examples, and typing tips.
