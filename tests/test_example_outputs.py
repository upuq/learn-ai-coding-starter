"""Exact-output tests for programs in examples/."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("equality.slop", "✅\n❌\n❌\n"),
        ("short-circuit.slop", "❌\n✅\n"),
    ],
)
def test_example_output(filename: str, expected: str):
    source = (EXAMPLES / filename).read_text(encoding="utf-8")
    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == expected
