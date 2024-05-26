""" Test file for dstatic.py script. """

from unittest import mock
import time

import pytest
from hecate import Runner

from dstatic import dstatic


def dstatic_cmd(*args):
    options = [a for a in args]
    return ["python3", "dstatic/dstatic.py"] + options


@pytest.mark.parametrize("color, expected", [
    ("all", 11), ("B&W", 20), ("red", 9), ("green", 10), ("blue", 10),
    ("yellow", 9), ("cyan", 9), ("magenta", 9)
])
def test_setup_colors_num_of_pairs(color, expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 256):
        result = dstatic.setup_curses_colors(color)
        assert result == expected


@pytest.mark.parametrize("color, expected", [
    ("all", 8), ("B&W", 8), ("red", 7), ("green", 7), ("blue", 7),
    ("yellow", 7), ("cyan", 7), ("magenta", 7)
])
def test_setup_colors_num_of_pairs_8_colors(color, expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 8):
        result = dstatic.setup_curses_colors(color)
        assert result == expected


@pytest.mark.parametrize("color, expected", [
    ("cyan", [(23, 23), (30, 30), (44, 44), (51, 51), (44, 44)]),
    ("all", [(16, 16), (255, 255), (40, 40), (184, 184), (164, 164)]),
    ("B&W", [(16, 16), (232, 232), (234, 234), (236, 236), (237, 237)]),
    ("yellow", [(58, 58), (94, 94), (106, 106), (184, 184), (184, 184)]),
])
def test_setup_curses_colors(color, expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 256):
        dstatic.setup_curses_colors(color)
        result = dstatic.curses.pair_content(1)
        assert result == (expected[0])
        result = dstatic.curses.pair_content(2)
        assert result == (expected[1])
        result = dstatic.curses.pair_content(4)
        assert result == (expected[2])
        result = dstatic.curses.pair_content(6)
        assert result == (expected[3])
        result = dstatic.curses.pair_content(7)
        assert result == (expected[4])


@pytest.mark.parametrize("color, expected", [
    ("cyan", [(6, 6), (6, 6), (6, 6), (7, 7), (0, 0)]),
    ("all", [(0, 0), (1, 1), (3, 3), (5, 5), (6, 6)]),
    ("B&W", [(0, 0), (7, 7), (7, 7), (7, 7), (0, 0)]),
    ("yellow", [(3, 3), (3, 3), (3, 3), (7, 7), (0, 0)]),
])
def test_setup_curses_colors_8_colors(color, expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 8):
        dstatic.setup_curses_colors(color)
        result = dstatic.curses.pair_content(1)
        assert result == (expected[0])
        result = dstatic.curses.pair_content(2)
        assert result == (expected[1])
        result = dstatic.curses.pair_content(4)
        assert result == (expected[2])
        result = dstatic.curses.pair_content(6)
        assert result == (expected[3])
        result = dstatic.curses.pair_content(7)
        assert result == (expected[4])


@pytest.mark.parametrize("color_list, expected", [
    (["B&W", "blue"], 30),
    (["B&W", "yellow", "red", "magenta"], 47),
    (["B&W", "red", "green", "blue", "yellow", "magenta", "cyan"], 76)
])
def test_setup_curses_colors_additive_num_of_pairs(color_list, expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 256):
        result = dstatic.setup_curses_colors_additive(color_list)
        assert result == expected


@pytest.mark.parametrize("color_list, expected", [
    (["B&W", "blue"], 15),
    (["B&W", "yellow", "red", "magenta"], 29),
    (["B&W", "red", "green", "blue", "yellow", "magenta", "cyan"], 50)
])
def test_setup_curses_colors_additive_num_of_pairs_8_colors(color_list,
                                                            expected):
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 8):
        result = dstatic.setup_curses_colors_additive(color_list)
        assert result == expected


def test_setup_curses_colors_additive():
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 256):
        dstatic.setup_curses_colors_additive(["B&W", "red"])
        assert dstatic.curses.pair_content(1) == (16, 16)
        assert dstatic.curses.pair_content(15) == (247, 247)
        assert dstatic.curses.pair_content(23) == (124, 124)


def test_setup_curses_colors_additive_8_colors():
    dstatic.curses.initscr()
    dstatic.curses.start_color()
    with mock.patch.object(dstatic.curses, "COLORS", 8):
        dstatic.setup_curses_colors_additive(["B&W", "red"])
        assert dstatic.curses.pair_content(1) == (0, 0)
        assert dstatic.curses.pair_content(9) == (1, 1)
        assert dstatic.curses.pair_content(15) == (0, 0)


def test_list_commands(capsys):
    dstatic.list_commands()
    captured_output = capsys.readouterr().out
    assert "List of running commands:" in captured_output
    assert " c                Toggle cycle color mode" in captured_output
    assert " r,t,y,u,i,o,p,[  Set single color" in captured_output


def test_list_colors(capsys):
    dstatic.list_colors()
    captured_output = capsys.readouterr().out
    expected_output = "Color List:\nred, green, blue, yellow, cyan, magenta\n"
    assert captured_output == expected_output
    assert "B&W" not in captured_output


def test_dstatic_test_mode():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_exit(test_key):
    """ Tests dstatic.py will exit on q or Q"""
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


def test_dstatic_exit_no_test_mode():
    with Runner(*dstatic_cmd()) as h:
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_black_and_white_mode():
    with Runner(*dstatic_cmd("--test_mode", "-b")) as h:
        h.await_text("B")


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_black_and_white_mode_quit(test_key):
    with Runner(*dstatic_cmd("--test_mode", "-b")) as h:
        h.await_text("B")
        h.write(test_key)
        h.press("enter")
        h.await_exit()


@pytest.mark.parametrize("test_color, expected", [
    ("red", "r"), ("green", "g"), ("blue", "b"), ("yellow", "y"),
    ("cyan", "c"), ("magenta", "m"),
])
def test_dstatic_color_mode(test_color, expected):
    with Runner(*dstatic_cmd("--test_mode", "-C", test_color)) as h:
        h.await_text(expected)


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_dstatic_color_quit(test_key):
    with Runner(*dstatic_cmd("--test_mode", "-C", "blue")) as h:
        h.await_text("b")
        h.write(test_key)
        h.press("enter")
        h.await_exit()


@pytest.mark.parametrize("test_delay", [
    "9", "8", "7", "6", "5", "4", "3", "2", "1", "0"
])
def test_dstatic_delay(test_delay):
    with Runner(*dstatic_cmd("--test_mode", "-d", test_delay)) as h:
        h.await_text("a")


def test_dstatic_delay_quit():
    with Runner(*dstatic_cmd("--test_mode", "-d", "9")) as h:
        h.await_text("a")
        h.press("Q")
        h.press("enter")
        h.await_exit()


def test_dstatic_start_timer_start():
    with Runner(*dstatic_cmd("--test_mode", "-s", "1")) as h:
        h.default_timeout = 2
        time.sleep(0.2)
        sc = h.screenshot()
        assert "a" not in sc
        h.await_text("a")


def test_dstatic_run_timer_runs():
    with Runner(*dstatic_cmd("--test_mode", "-r", "2")) as h:
        h.default_timeout = 3
        h.await_text("a")
        time.sleep(1)
        h.await_text("a")


def test_dstatic_run_timer_auto_exits():
    with Runner(*dstatic_cmd("--test_mode", "-r", "2")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.await_exit()


def test_dstatic_run_timer_quit_key():
    with Runner(*dstatic_cmd("--test_mode", "-r", "2")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.write("q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_screen_saver_mode_runs():
    with Runner(*dstatic_cmd("--test_mode", "-S")) as h:
        h.await_text("a")


@pytest.mark.parametrize("key", [
    "a", "b", "d", "R", "B", "Q", "i", "7", "#", "q", "P", " ", "=", "c", "C"
])
def test_dstatic_screen_saver_mode_any_key_exit(key):
    with Runner(*dstatic_cmd("--test_mode", "-S")) as h:
        h.await_text("a")
        h.write(key)
        h.press("Enter")
        h.await_exit()


def test_dstatic_screen_saver_run_timer_exit():
    with Runner(*dstatic_cmd("--test_mode", "-S", "-r", "2")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.await_exit()


@pytest.mark.parametrize("cmd, size_change", [
    ('-vt0', 20), ('-vt0', 46), ('-vt0', 47),
    ('-ht0', 46), ('-ht0', 48), ('-ht0', 49)
])
def test_dstatic_resize(cmd, size_change):
    with Runner(*dstatic_cmd("--test_mode"), width=50, height=50) as h:
        h.await_text("a")
        h.tmux.execute_command('split-window', cmd, '-l', size_change)
        h.await_text("a")


def test_dstatic_cycle_colors():
    with Runner(*dstatic_cmd("--test_mode", "-c")) as h:
        h.default_timeout = 3
        h.await_text("r")
        h.await_text("g")
        h.await_text("b")


def test_dstatic_cycle_colors_quit():
    with Runner(*dstatic_cmd("--test_mode", "-c")) as h:
        h.default_timeout = 3
        h.await_text("r")
        h.await_text("g")
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_additive_mode_run():
    with Runner(*dstatic_cmd("--test_mode", "-a")) as h:
        h.await_text("A")


def test_dstatic_additive_mode_run_quit():
    with Runner(*dstatic_cmd("--test_mode", "-a")) as h:
        h.await_text("A")
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_disable_keys_still_quits():
    with Runner(*dstatic_cmd("--test_mode", "-D")) as h:
        h.await_text("a")
        h.write("Q")
        h.press("Enter")
        h.await_exit()


def test_dstatic_disable_all_keys_q_does_not_quit():
    with Runner(*dstatic_cmd("--test_mode", "--disable_all_keys")) as h:
        h.await_text("a")
        h.write("Q")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_disable_all_keys_ctrl_c_quits():
    with Runner("bash") as h:
        h.await_text("$")
        h.write("python3 dstatic/dstatic.py --test_mode --disable_all_keys")
        h.press("Enter")
        h.await_text("a")
        h.press("C-c")
        h.await_text("$")


def test_dstatic_disable_keys_does_not_affect_screen_saver_mode():
    with Runner(*dstatic_cmd("--test_mode", "-S", "-D")) as h:
        h.await_text("a")
        h.write("b")
        h.press("Enter")
        h.await_exit()


def test_dstatic_disable_all_keys_does_not_affect_screen_saver_mode():
    with Runner(*dstatic_cmd("--test_mode", "-S", "--disable_all_keys")) as h:
        h.await_text("a")
        h.write("b")
        h.press("Enter")
        h.await_exit()


def test_dstatic_list_commands(capsys):
    return_value = dstatic.main(["--list_commands"])
    captured_output = capsys.readouterr().out
    assert "List of running commands:" in captured_output
    assert return_value == 0


def test_dstatic_list_colors(capsys):
    return_value = dstatic.main(["--list_colors"])
    captured_output = capsys.readouterr().out
    assert "Color List:" in captured_output
    assert return_value == 0


def test_dstatic_help_version(capsys):
    with pytest.raises(SystemExit):
        dstatic.main(["--version"])
    captured_output = capsys.readouterr().out
    assert f"{dstatic.VERSION}\n" == captured_output


def test_dstatic_display_help():
    with Runner(*dstatic_cmd("--help"), width=80, height=40) as h:
        h.await_text("usage:")
        sc = h.screenshot()
        assert "dstatic" in sc


def test_dstatic_display_help_no_test_mode():
    with Runner(*dstatic_cmd("--help"), width=80, height=40) as h:
        h.await_text("usage:")
        sc = h.screenshot()
        assert "--test_mode" not in sc


def test_dstatic_toggle_black_and_white():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")
        h.write("b")
        h.press("Enter")
        h.await_text("B")
        h.write("b")
        h.press("Enter")
        h.await_text("a")


@pytest.mark.parametrize("option, await_char", [
    ("-b", "B"), ("-c", "r"), ("-a", "A")
])
def test_dstatic_color_mode_command(option, await_char):
    with Runner(*dstatic_cmd("--test_mode", option)) as h:
        h.await_text(await_char)
        h.write("C")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_toggle_cycle_color_mode():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")
        h.write("c")
        h.press("Enter")
        h.await_text("r")
        h.write("c")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_toggle_additive_color_mode():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.write("a")
        h.press("Enter")
        h.await_text("A")
        time.sleep(2)
        h.write("a")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_additive_color_mode_colors():
    with Runner(*dstatic_cmd("--test_mode", "-a")) as h:
        h.await_text("A")
        h.write("r")
        h.press("Enter")
        h.await_text("A")
        sc = h.screenshot()
        assert "r" not in sc


def test_dstatic_default_command():
    with Runner(*dstatic_cmd("--test_mode", "-C", "green")) as h:
        h.await_text("g")
        h.write("d")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_change_delay_speed():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")
        h.write("9")
        h.press("Enter")
        h.await_text("a")
        h.write("7")
        h.press("Enter")
        h.await_text("a")
        h.write("4")
        h.press("Enter")
        h.await_text("a")
        h.write("2")
        h.press("Enter")
        h.await_text("a")
        h.write("0")
        h.press("Enter")
        h.await_text("a")


def test_dstatic_cycle_color_time():
    with Runner(*dstatic_cmd("--test_mode", "-c")) as h:
        h.default_timeout = 5
        h.await_text("r")
        h.write("%")
        h.press("Enter")
        h.await_text("g")
        h.write("!")
        h.press("Enter")
        h.await_text("b")


def test_dstatic_single_color_change():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.await_text("a")
        h.write("r")
        h.press("Enter")
        h.await_text("r")
        h.write("t")
        h.press("Enter")
        h.await_text("g")
        h.write("u")
        h.press("Enter")
        h.await_text("y")
        h.write("o")
        h.press("Enter")
        h.await_text("c")
        h.write("y")
        h.press("Enter")
        h.await_text("b")
        h.write("i")
        h.press("Enter")
        h.await_text("m")
        h.write("r")
        h.press("Enter")
        h.await_text("r")


def test_dstatic_disable_keys_not_working():
    with Runner(*dstatic_cmd("--test_mode", "-D")) as h:
        h.await_text("a")
        h.write("y")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "b" not in sc
        h.write("b")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "B" not in sc
        h.write("a")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "A" not in sc


def test_dstatic_disable_all_keys_not_working():
    with Runner(*dstatic_cmd("--test_mode", "--disable_all_keys")) as h:
        h.await_text("a")
        h.write("o")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "c" not in sc
        h.write("a")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "A" not in sc
        h.write("i")
        h.press("Enter")
        h.await_text("a")
        sc = h.screenshot()
        assert "m" not in sc


def test_dstatic_disable_keys_keys_not_working_default():
    with Runner(*dstatic_cmd("--test_mode", "-D", "-b")) as h:
        h.await_text("B")
        h.write("d")
        h.press("Enter")
        h.await_text("B")
        sc = h.screenshot()
        assert "a" not in sc


def test_dstatic_disable_all_keys_keys_not_working_default():
    with Runner(*dstatic_cmd("--test_mode", "--disable_all_keys", "-a")) as h:
        h.await_text("A")
        h.write("d")
        h.press("Enter")
        h.await_text("A")
        sc = h.screenshot()
        assert "a" not in sc


def test_dstatic_clear_screen():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.write("l")
        h.press("Enter")
        time.sleep(0.2)
        sc = h.screenshot()
        assert "a" not in sc
        h.await_text("a")


def test_dstatic_freeze_screen():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.write("f")
        h.press("Enter")
        time.sleep(0.1)
        sc1 = h.screenshot()
        time.sleep(0.5)
        sc2 = h.screenshot()
        assert sc1 == sc2
        h.write("f")
        h.press("Enter")
        time.sleep(0.1)
        sc3 = h.screenshot()
        assert sc3 != sc2


def test_dstatic_freeze_screen_no_other_commands_working():
    with Runner(*dstatic_cmd("--test_mode")) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.write("f")
        h.press("Enter")
        time.sleep(0.1)
        sc1 = h.screenshot()
        h.write("r")
        h.press("Enter")
        time.sleep(0.1)
        assert h.screenshot() == sc1


def test_dstatic_test_pattern1():
    with Runner(*dstatic_cmd("--test_mode"), width=30, height=10) as h:
        h.await_text("a")
        h.press("z")
        h.await_text("w")
        sc = h.screenshot()
        assert "wwwyyycccgggmmmrrrbbbBBB" in sc
        expect = ("wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n"
                  "wwwyyycccgggmmmrrrbbbBBB\n\n")
        assert sc == expect


def test_dstatic_test_pattern2():
    with Runner(*dstatic_cmd("--test_mode"), width=30, height=20) as h:
        h.default_timeout = 2
        h.await_text("a")
        h.press("z")
        h.press("enter")
        h.await_text("w")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("y")
        time.sleep(0.5)
        sc = h.screenshot()
        assert "wwwwyyyyccccggggmmmmrrrrbbbb" in sc
        assert "wwwyyycccgggmmmrrrbbbBBB" not in sc
        expect = """wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
wwwwyyyyccccggggmmmmrrrrbbbb
BBBBbbbbrrrrmmmmggggccccyyyy\n
"""
        assert sc == expect


def test_dstatic_test_pattern3():
    with Runner(*dstatic_cmd("--test_mode"), width=42, height=20) as h:
        h.default_timeout = 2
        h.await_text("a")
        h.press("z")
        h.press("enter")
        h.await_text("w")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("y")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("y")
        time.sleep(0.5)
        sc = h.screenshot()
        assert "wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb" in sc
        assert "wwwwyyyyccccggggmmmmrrrrbbbb" not in sc
        expect = """wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
wwwwwwyyyyyyccccccggggggmmmmmmrrrrrrbbbbbb
bbbbbbbbbbbbwwbbbbbbbbbbbb
bbbbbbbbbbbbwwbbbbbbbbbbbb
bbbbbbbbbbbbwwbbbbbbbbbbbb
bbbbbbbbbbbbwwbbbbbbbbbbbb
bbbbbbbbbbbbwwbbbbbbbbbbbb\n
"""
        print(sc)
        assert sc == expect


def test_dstatic_test_pattern_cycle_back_to_normal():
    with Runner(*dstatic_cmd("--test_mode"), width=42, height=20) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.press("z")
        h.press("enter")
        h.await_text("w")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("y")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("y")
        time.sleep(0.5)
        h.press("z")
        h.press("enter")
        h.await_text("a")
        time.sleep(0.5)
        sc = h.screenshot()
        assert "w" not in sc


def test_dstatic_blue_screen():
    with Runner(*dstatic_cmd("--test_mode"), width=78, height=23) as h:
        h.default_timeout = 3
        h.await_text("a")
        h.press("w")
        h.press("enter")
        h.await_text("A problem has been")
        time.sleep(0.5)
        h.press("w")
        h.press("enter")
        h.await_text("a")
        time.sleep(0.25)
        sc = h.screenshot()
        assert "A problem has been" not in sc
