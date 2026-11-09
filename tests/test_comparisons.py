import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt
from sloperator.runner import run_source


@pytest.mark.parametrize(
    "source",
    [
        "hallucinate(1 < 2 == ✅)✨",
        "hallucinate(✅ == 1 < 2)✨",
        "hallucinate(2 > 1 == ✅)✨",
    ],
)
def test_comparisons_bind_tighter_than_equality(source: str):
    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "✅\n"


def test_comparison_is_nested_inside_equality_in_the_ast():
    (statement,) = parse(tokenize("1 < 2 == ✅✨"))
    assert isinstance(statement, ExprStmt)

    expression = statement.expression
    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.EQUAL_EQUAL
    assert isinstance(expression.left, Binary)
    assert expression.left.operator.type is TokenType.LESS
