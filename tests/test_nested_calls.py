from sloperator.runner import run_source


def test_call_used_directly_as_an_argument_to_another_call():
    source = """clanker double(n) {
    ship n * 2✨
}
clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(double(1), double(2)))✨"""

    result = run_source(source)

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "6\n"


def test_nested_call_as_the_only_argument():
    source = """clanker double(n) {
    ship n * 2✨
}
hallucinate(double(double(5)))✨"""

    result = run_source(source)

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "20\n"
