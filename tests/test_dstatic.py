""" Test file for dstatic.py script. """

from unittest import mock

import pytest
from hecate import Runner

from dstatic import dstatic


def dstatic_cmd(*args):
    options = [a for a in args]
    return ["python3", "dstatic/dstatic.py"] + options


@pytest.mark.parametrize("test_values, expected_results", [
    (0, 0), (1, 0.01), (2, 0.03), (3, 0.06), (4, 0.1),
    (5, 0.15), (6, 0.21), (7, 0.28), (8, 0.36), (9, 0.45)
])
def test_convert_delay_number_to_delay_time(test_values, expected_results):
    result = dstatic.convert_delay_number_to_delay_time(test_values)
    assert result == expected_results


@pytest.mark.parametrize("test_mode", [
    "color", "bw", "black", "green", "red"
])
def test_set_curses_color_mock_call(test_mode):
    with mock.patch.object(dstatic.curses, "init_pair", return_value=None) as mock_init:
        dstatic.set_curses_colors(test_mode)
        call_count = mock_init.call_count
        assert call_count == 8


def test_set_curses_colors():
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    dstatic.set_curses_colors("cyan")
    result = dstatic.curses.pair_content(8)
    assert result == (dstatic.curses.COLOR_CYAN, dstatic.curses.COLOR_CYAN)
    result = dstatic.curses.pair_content(1)
    assert result == (dstatic.curses.COLOR_CYAN, dstatic.curses.COLOR_CYAN)
    result = dstatic.curses.pair_content(5)
    assert result == (dstatic.curses.COLOR_CYAN, dstatic.curses.COLOR_CYAN)


def test_set_curses_colors_bw():
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    dstatic.set_curses_colors("bw")
    result = dstatic.curses.pair_content(1)
    assert result == (dstatic.curses.COLOR_BLACK, dstatic.curses.COLOR_BLACK)
    result = dstatic.curses.pair_content(4)
    assert result == (dstatic.curses.COLOR_BLACK, dstatic.curses.COLOR_BLACK)
    result = dstatic.curses.pair_content(5)
    assert result == (dstatic.curses.COLOR_WHITE, dstatic.curses.COLOR_WHITE)
    result = dstatic.curses.pair_content(8)
    assert result == (dstatic.curses.COLOR_WHITE, dstatic.curses.COLOR_WHITE)


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit(test_key):
    """ Tests dstatic.py will exit on q or Q"""
    with Runner(*dstatic_cmd()) as h:
        h.await_text(chr(9617))
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit_delay_set(test_key):
    """
    Tests dstatic.py will exit on q or Q
    when setting delay time
    """
    with Runner(*dstatic_cmd("-d1")) as h:
        h.await_text(chr(9617))
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit_black_white_mode(test_key):
    """
    Tests dstatic.py will exit on q or Q
    when using black and white mode
    """
    with Runner(*dstatic_cmd("-b")) as h:
        h.await_text(chr(9617))
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit_start_timer(test_key):
    """
    Tests dstatic.py will exit on q or Q
    when using start timer
    """
    with Runner(*dstatic_cmd("-s1")) as h:
        h.default_timeout = 2
        h.await_text(chr(9617))
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit_delay_set(test_key):
    """
    Tests dstatic.py will exit on q or Q
    when using run timer.
    """
    with Runner(*dstatic_cmd("-r1")) as h:
        h.await_text(chr(9617))
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_dstatic_run_timer_exit():
    """ Test auto exit when using run timer. """
    with Runner(*dstatic_cmd("-r2")) as h:
        h.default_timeout = 3
        h.await_text(chr(9617))
        h.await_exit()


def test_dstatic_start_timer():
    """ Test start timer."""
    with Runner(*dstatic_cmd("-s2")) as h:
        h.default_timeout = 3
        h.await_text(chr(9617))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_keys", [
    " ", "h", "H", "8", ";", "q",  "e", "*", "", "'", "0", "!",
])
def test_dstatic_exit_screen_save_mode(test_keys):
    """
    Test a same of any key will exit dstatic
    in screen save mode.
    """
    with Runner(*dstatic_cmd("-S")) as h:
        h.await_text(chr(9617))
        h.write(test_keys)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("cmd, size_change", [
    ('-vt0', 20), ('-vt0', 46), ('-vt0', 47),
    ('-ht0', 46), ('-ht0', 48), ('-ht0', 49)
])
def test_dstatic_resize(cmd, size_change):
    with Runner(*dstatic_cmd("--test_mode"), width=50, height=50) as h:
        h.await_text("0")
        h.tmux.execute_command('split-window', cmd, '-l', size_change)
        h.await_text("0")


def test_black_and_white_command():
    with Runner(*dstatic_cmd()) as h:
        h.write("b")
        h.press("Enter")
        h.await_text(chr(9617))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_red_color_command():
    with Runner(*dstatic_cmd()) as h:
        h.write("r")
        h.press("Enter")
        h.await_text(chr(9617))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_cycle_color_command():
    with Runner(*dstatic_cmd()) as h:
        h.write("c")
        h.press("Enter")
        h.await_text(chr(9617))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_color_command():
    with Runner(*dstatic_cmd()) as h:
        h.write("C")
        h.press("Enter")
        h.await_text(chr(9617))
        h.write("Q")
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_value", ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
def test_delay_change(test_value):
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.default_timeout = 2
        h.await_text("0")
        h.write(test_value)
        h.press("Enter")
        h.await_text("0")
        h.write("4")
        h.press("Enter")
        h.await_text("0")
        h.write("Q")
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("expected_results",
                         [chr(9617), chr(9618), chr(9619), chr(9608), " "])
def test_block_special_char(expected_results):
    with Runner(*dstatic_cmd()) as h:
        h.default_timeout = 2
        h.await_text(expected_results)
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_list_commands():
    with Runner(*dstatic_cmd("--list_commands")) as h:
        h.await_text("List of running commands:")


def test_dstatic_list_colors():
    with Runner(*dstatic_cmd("--list_colors")) as h:
        h.await_text("Color List:")
