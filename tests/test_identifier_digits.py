from sloperator.lexer import TokenType, tokenize
from sloperator.runner import run_source


def test_identifier_can_contain_digits():
    tokens = tokenize("score2")

    assert tokens[0].type is TokenType.IDENTIFIER
    assert tokens[0].lexeme == "score2"


def test_identifier_cannot_start_with_a_digit():
    tokens = tokenize("2score")

    assert [token.type for token in tokens] == [
        TokenType.NUMBER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]
    assert tokens[0].literal == 2
    assert tokens[1].lexeme == "score"


def test_declaration_cannot_start_with_a_digit():
    result = run_source("slop 2score = 1✨")

    assert result.exit_code == 1
    assert result.stderr.startswith(
        "SlopLang syntax error at line 1: expected a variable name after 'slop', found '2'"
    )


def test_variable_names_can_contain_digits():
    source = """slop score2 = 40✨
score2 = score2 + 2✨
hallucinate(score2)✨"""

    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "42\n"


def test_function_and_parameter_names_can_contain_digits():
    source = """clanker add2(value1, value2) {
    ship value1 + value2✨
}
hallucinate(add2(40, 2))✨"""

    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "42\n"
