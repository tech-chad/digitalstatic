
import pytest

from dstatic import dstatic


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


@pytest.mark.parametrize("test_value", [
    "red", "green", "blue", "magenta", "yellow", "cyan",
])
def test_color_type_normal(test_value):
    result = dstatic.color_type(test_value)
    assert result == test_value


@pytest.mark.parametrize("test_values", [
    "purple", "orange", "color", "word", "12345", "", " ", "*(#", "B&W"
])
def test_color_type_error(test_values):
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.color_type(test_values)


@pytest.mark.parametrize("test_values, expected_result", [
    ("1", 1),
    ("100", 100),
    ("20000000", 20000000)
])
def test_pos_int(test_values, expected_result):
    result = dstatic.pos_int(test_values)
    assert result == expected_result


@pytest.mark.parametrize("test_values", [
    "0", "-1", "-40000", "10.6", "-2.6", "A", "letters", "*", "$", "0.0"
])
def test_pos_int_error(test_values):
    with pytest.raises(dstatic.argparse.ArgumentTypeError):
        dstatic.pos_int(test_values)


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 4), (["-d0"], 0), (["-d 1"], 1), (["-d", "2"], 2),
    (["-d3"], 3), (["-d 4"], 4), (["-d", "5"], 5), (["-d6"], 6),
    (["-d 7"], 7), (["-d", "8"], 8), (["-d9"], 9)
])
def test_parser_arguments_delay(test_values, expected_results):
    """ Testing a single argument -d (delay option). """
    result = dstatic.argument_parser(test_values)
    assert result.delay == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-b"], True)
])
def test_parser_arguments_black_white(test_values, expected_results):
    """ Testing single argument -b (black & white mode). """
    result = dstatic.argument_parser(test_values)
    assert result.black_white == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-s 5"], 5), (["-s500"], 500)
])
def test_argument_parsing_start(test_values, expected_results):
    """ Testing single argument -s SECONDS (start timer option). """
    result = dstatic.argument_parser(test_values)
    assert result.start_timer == expected_results


def test_argument_parsing_start_timer_long_command():
    result = dstatic.argument_parser(["--start_timer", "5"])
    assert result.start_timer == 5


@pytest.mark.parametrize("test_values, expected_results", [
    ([], 0), (["-r20"], 20), (["-r500"], 500)
])
def test_argument_parsing_run(test_values, expected_results):
    """ Testing single argument -r SECONDS (run timer option). """
    result = dstatic.argument_parser(test_values)
    assert result.run_timer == expected_results


def test_argument_parsing_run_long_command():
    result = dstatic.argument_parser(["--run_timer", "5"])
    assert result.run_timer == 5


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-S"], True), (["--screen_saver"], True)
])
def test_argument_parsing_screen_saver(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.screen_saver == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_commands"], True)
])
def test_argument_parsing_list_commands(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.list_commands == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], None), (["-C", "red"], "red"), (["-C", "yellow"], "yellow")
])
def test_argument_parsing_color(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.color == expected_results


def test_argument_parsing_color_long_option():
    result = dstatic.argument_parser(["--color", "blue"])
    assert result.color == "blue"


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--list_colors"], True)
])
def test_argument_parsing_list_commands(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.list_colors == expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["--test_mode"], True)
])
def test_argument_parsing_test_mode(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.test_mode is expected_results


@pytest.mark.parametrize("test_values, expected_results", [
    ([], False), (["-c"], True), (["--cycle_colors"], True)
])
def test_argument_parsing_cycle_colors(test_values, expected_results):
    result = dstatic.argument_parser(test_values)
    assert result.cycle_color_mode is expected_results


@pytest.mark.parametrize("test_values, expected_result", [
    ([], False), (["-a"], True), (["--additive"], True)
])
def test_argument_parsing_additive_color_mode(test_values, expected_result):
    result = dstatic.argument_parser(test_values)
    assert result.additive is expected_result


@pytest.mark.parametrize("test_values, expected_result", [
    ([], False), (["-D"], True), (["--disable_keys"], True),
])
def test_argument_parsing_disable_keys(test_values, expected_result):
    result = dstatic.argument_parser(test_values)
    assert result.disable_keys is expected_result


@pytest.mark.parametrize("test_values, expected_result", [
    ([], False), (["--disable_all_keys"], True),
])
def test_argument_parsing_disable_all_keys(test_values, expected_result):
    result = dstatic.argument_parser(test_values)
    assert result.disable_all_keys is expected_result


def test_argument_parsing_version(capsys):
    with pytest.raises(SystemExit):
        dstatic.argument_parser(["--version"])
    captured_output = capsys.readouterr().out
    assert f"{dstatic.VERSION}\n" == captured_output
