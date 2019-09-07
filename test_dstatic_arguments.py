
import pytest

import dstatic


@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 0.01), ("2", 0.03), ("3", 0.06), ("4", 0.1),
    ("5", 0.15), ("6", 0.21), ("7", 0.28), ("8", 0.36), ("9", 0.45)
])
def test_delay_positive_int_normal(test_values, expected_results):
    result = dstatic.delay_positive_int(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "-5", "10", "100", "2.5", " ", "Test", "test&*#"
])
def test_delay_positive_int_error(test_values):
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.delay_positive_int(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ("1", 1), ("5", 5), ("10", 10), ("25", 25), ("99", 99), ("500", 500),
    ("7865432549", 7865432549)
])
def test_positive_int_normal(test_values, expected_results):
    result = dstatic.positive_int(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "0", "-3", "3.5", "-3.5", "trash", "#$@#"
])
def test_positive_int_error(test_values):
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.positive_int(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0.1), (["-d0"], 0), (["-d 1"], 0.01), (["-d", "2"], 0.03), (["-d3"], 0.06),
    (["-d 4"], 0.1), (["-d", "5"], 0.15), (["-d6"], 0.21), (["-d 7"], 0.28), (["-d", "8"], 0.36),
    (["-d9"], 0.45)
])
def test_parser_arguments_delay(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.delay == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-b"], True)
])
def test_parser_arguments_black_white(test_values,expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.black_white == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-s 5"], 5), (["-s500"], 500)
])
def test_argument_parsing_start(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.start_timer == expected_results
