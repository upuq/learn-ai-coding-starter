import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


def test_lexical_error_after_em_dash_comment_reports_later_line():
    with pytest.raises(LexicalError) as info:
        tokenize('— a comment\n"hi"✨')

    assert info.value.line == 2
    assert info.value.message == "straight quotes are not supported, use “ and ” for strings"
    assert str(info.value) == (
        "SlopLang lexical error at line 2: "
        "straight quotes are not supported, use “ and ” for strings"
    )
