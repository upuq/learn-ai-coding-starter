"""Regression tests for variable assignment in nested block scopes."""

from sloperator.runner import run_source


def test_assignment_updates_nearest_enclosing_scope():
    source = """\
slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨
"""

    result = run_source(source)

    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == "3\n1\n"
