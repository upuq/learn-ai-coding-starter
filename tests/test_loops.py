from sloperator.runner import run_source


def test_false_condition_runs_the_loop_zero_times():
    source = """ralph ❌ {
    hallucinate(“never”)✨
}"""

    result = run_source(source)

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == ""
