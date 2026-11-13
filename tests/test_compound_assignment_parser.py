from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Literal, VarDecl


def parse_source(source: str):
    return parse(tokenize(source))


def test_plus_equal_is_a_single_greedy_token():
    tokens = tokenize("+ +=")
    assert [token.type for token in tokens] == [
        TokenType.PLUS,
        TokenType.PLUS_EQUAL,
        TokenType.EOF,
    ]


def test_compound_assignment_parses_as_assign_with_inner_expression():
    declaration, assignment = parse_source("slop n = 2✨\nn += 3 * 4✨\n")

    assert isinstance(declaration, VarDecl)
    assert isinstance(assignment, Assign)
    assert assignment.name.lexeme == "n"
    assert assignment.operator.type is TokenType.PLUS_EQUAL

    value = assignment.value
    assert isinstance(value, Binary) and value.operator.type is TokenType.STAR
    assert isinstance(value.left, Literal) and value.left.value == 3
    assert isinstance(value.right, Literal) and value.right.value == 4
