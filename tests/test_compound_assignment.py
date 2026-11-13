"""Runtime behavior of compound assignment with +=."""

import pytest

from sloperator.runner import run_source


def test_compound_assignment_evaluates_rhs_then_adds():
    result = run_source("slop n = 2✨\nn += 3 * 4✨\nhallucinate(n)✨")

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "14\n"


def test_compound_assignment_uses_current_value_while_evaluating_rhs():
    result = run_source("slop n = 2✨\nn += n * 2✨\nhallucinate(n)✨")

    assert result.exit_code == 0, result.stderr
    assert result.stdout == "6\n"


def test_compound_assignment_concatenates_strings():
    result = run_source(
        "slop greeting = “hello”✨\ngreeting += “, slop”✨\nhallucinate(greeting)✨"
    )

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "hello, slop\n"


def test_compound_assignment_updates_nearest_binding():
    source = """\
slop score = 1✨
{
    slop score = 2✨
    {
        score += 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨
"""
    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "5\n1\n"


@pytest.mark.parametrize(
    ("source", "line", "message"),
    [
        ("missing += 1✨", 1, "undefined variable 'missing'"),
        (
            "loadbearing MAX = 3✨\nMAX += 1✨",
            2,
            "cannot assign to loadbearing 'MAX'",
        ),
        (
            "slop n = 1✨\nn += “text”✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got number and string",
        ),
        (
            "slop text = “a”✨\ntext += 1✨",
            2,
            "operands of '+=' must both be numbers or both be strings, got string and number",
        ),
    ],
)
def test_compound_assignment_runtime_errors(source: str, line: int, message: str):
    result = run_source(source)

    assert result.exit_code == 1
    assert result.stderr == f"SlopLang runtime error at line {line}: {message}\n"
