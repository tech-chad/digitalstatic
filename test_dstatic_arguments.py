
import pytest

import dstatic


@pytest.mark.parametrize("test_values, expected_results", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9)
])
def test_positive_int_zero_to_nine_normal(test_values, expected_results):
    """ Tests that the delay time conversion formula is working. """
    result = dstatic.positive_int_zero_to_nine(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_values", [
    "-5", "10", "100", "2.5", " ", "Test", "test&*#", "",
])
def test_positive_int_zero_to_nine_error(test_values):
    """ Testing delay_positive_int will raise an error. """
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.positive_int_zero_to_nine(test_values)


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


@pytest.mark.parametrize("test_value", [
    "red", "green", "blue", "magenta", "yellow", "cyan", "black"
])
def test_color_type_normal(test_value):
    result = dstatic.color_type(test_value)
    assert result == test_value


@pytest.mark.parametrize("test_values", [
    "purple", "orange", "color", "word", "12345", "", " ", "*(#"
])
def test_color_type_error(test_values):
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.color_type(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 4), (["-d0"], 0), (["-d 1"], 1), (["-d", "2"], 2),
    (["-d3"], 3), (["-d 4"], 4), (["-d", "5"], 5), (["-d6"], 6),
    (["-d 7"], 7), (["-d", "8"], 8), (["-d9"], 9)
])
def test_parser_arguments_delay(test_values, expected_results):
    """ Testing a single argument -d (delay option). """
    result = dstatic.argument_parsing(test_values)
    assert result.delay == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-b"], True)
])
def test_parser_arguments_black_white(test_values,expected_results):
    """ Testing single argument -b (black & white mode). """
    result = dstatic.argument_parsing(test_values)
    assert result.black_white == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-s 5"], 5), (["-s500"], 500)
])
def test_argument_parsing_start(test_values, expected_results):
    """ Testing single argument -s SECONDS (start timer option). """
    result = dstatic.argument_parsing(test_values)
    assert result.start_timer == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-r20"], 20), (["-r500"], 500)
])
def test_argument_parsing_run(test_values, expected_results):
    """ Testing single argument -r SECONDS (run timer option). """
    result = dstatic.argument_parsing(test_values)
    assert result.run_timer == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-S"], True)
])
def test_argument_parsing_screen_saver(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.screen_saver == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_commands"], True)
])
def test_argument_parsing_list_commands(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.list_commands == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], None), (["-C", "red"], "red"), (["-C", "yellow"], "yellow")
])
def test_argument_parsing_color(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.color == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_colors"], True)
])
def test_argument_parsing_list_commands(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.list_colors == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--test_mode"], True)
])
def test_argument_parsing_test_mode(test_values, expected_results):
    result = dstatic.argument_parsing(test_values)
    assert result.test_mode is expected_results

