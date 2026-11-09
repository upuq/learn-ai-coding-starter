import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“” + “slop”", "slop"),
        ("“slop” + “”", "slop"),
        ("“café” + “✨”", "café✨"),
    ],
)
def test_string_addition(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_string_addition_example_program():
    source = """hallucinate(“” + “slop”)✨
— slop
hallucinate(“slop” + “”)✨
— slop

hallucinate(“café” + “✨”)✨
— café✨"""
    assert run(source) == "slop\nslop\ncafé✨\n"
