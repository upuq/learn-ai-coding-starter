---
name: create-test-program
description: Create a runnable SlopLang example for a language feature and lock its output with an exact-output test in tests/test_example_outputs.py
---

# Create Test Program

Given a language feature, create a small runnable SlopLang program that demonstrates it and add an exact-output test for that program.

## Workflow

1. Read `docs/spec.md` and identify the feature's syntax, semantics, and output formatting. The spec is the source of truth.
2. Write `examples/<feature>.slop`. Use smart quotes (`“…”`) for strings, end every statement with `✨`, and print values with `hallucinate(value)✨`.
3. Run the example from the project root and capture its exact output:
   `uv run sloperator.py examples/<feature>.slop`
4. Add one case to the parameter list in `tests/test_example_outputs.py`, mapping the filename to the exact expected stdout. If the file does not exist, create it with the shape below. Preserve existing cases.
5. Run `uv run pytest tests/test_example_outputs.py -q`, then run the project validation checks in `.agents/skills/validate/SKILL.md`.

## Exact-output test shape

`tests/test_example_outputs.py` is a parameterized test over example files:

```python
from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        # One row per example. Replace this placeholder with the new case;
        # keep rows that already exist.
        ("<example>.slop", "<exact stdout including trailing newline>"),
    ],
)
def test_example_output(filename: str, expected: str):
    source = (EXAMPLES / filename).read_text(encoding="utf-8")
    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == expected
```

When creating the file for the first time, replace the placeholder row with the new example's filename and exact output. Keep the expected string exact, including the trailing newline for every printed value. Add new cases to the existing parameter list; do not replace earlier cases.

## Rules

- Do not invent syntax. If the spec is ambiguous, report the ambiguity instead of guessing.
- Do not modify unrelated examples or tests.
- The example must be deterministic and print at least one line.
