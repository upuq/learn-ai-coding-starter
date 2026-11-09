import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_not_flips_booleans():
    assert run("hallucinate(!✅, !❌, !!✅)✨") == "❌ ✅ ✅\n"


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("!✅", "❌"),
        ("!❌", "✅"),
        ("!!✅", "✅"),
        ("!!❌", "❌"),
        ("!(!✅)", "✅"),
        ("!(1 < 2)", "❌"),
    ],
)
def test_not_expressions(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("hallucinate(!1)✨", 1, "operand of unary '!' must be a boolean, got number"),
        ("hallucinate(!“text”)✨", 1, "operand of unary '!' must be a boolean, got string"),
        (
            "clanker nothing() { }\nhallucinate(!nothing())✨",
            2,
            "operand of unary '!' must be a boolean, got nil",
        ),
    ],
)
def test_not_requires_a_boolean(source: str, line: int, message: str):
    assert fails(source) == f"SlopLang runtime error at line {line}: {message}"
