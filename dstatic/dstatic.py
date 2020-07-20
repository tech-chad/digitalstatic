#! /usr/bin/python3
""" Snow / static simulation using curses. """

import argparse
import curses
import datetime
import os
import sys
from random import randint
from random import choice
from time import sleep

from typing import List
from typing import Optional
from typing import Sequence

import argparse_types  # type: ignore

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata  # type: ignore

version = importlib_metadata.version("digital_static")

curses_number_ch_codes = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55:
                          7, 56: 8, 57: 9}
curses_shift_num_codes = {33: 1, 64: 2, 35: 3, 36: 4, 37: 5}
curses_ch_codes_color = {114: "red", 116: "green", 121: "blue", 117: "yellow",
                         105: "magenta", 111: "cyan", 112: "white", 91: "black"}
CURSES_COLORS = {"black": curses.COLOR_BLACK, "white": curses.COLOR_WHITE,
                 "blue": curses.COLOR_BLUE, "green": curses.COLOR_GREEN,
                 "magenta": curses.COLOR_MAGENTA, "yellow": curses.COLOR_YELLOW,
                 "red": curses.COLOR_RED, "cyan": curses.COLOR_CYAN}
if os.environ.get("TERM") == "linux":
    block_list = [" "]
else:
    block_list = [chr(9617), chr(9618), chr(9619), chr(9608), " "]


def set_curses_colors(mode: str, additive_colors: List[str]) -> None:
    """ Set curses colors. """
    if mode == "color":
        for i, color in enumerate(CURSES_COLORS.keys()):
            curses.init_pair(i + 1, CURSES_COLORS[color], CURSES_COLORS[color])
    elif mode == "bw":
        for i in range(1, 5):
            curses.init_pair(i, CURSES_COLORS["black"], CURSES_COLORS["black"])
        for i in range(5, 9):
            curses.init_pair(i, CURSES_COLORS["white"], CURSES_COLORS["white"])
    elif mode == "additive":
        if len(additive_colors) == 1:
            for i in range(1, 9):
                curses.init_pair(i, CURSES_COLORS[additive_colors[0]],
                                 CURSES_COLORS[additive_colors[0]])
        elif len(additive_colors) == 2:
            for i in range(1, 5):
                curses.init_pair(i, CURSES_COLORS[additive_colors[0]],
                                 CURSES_COLORS[additive_colors[0]])
            for i in range(5, 9):
                curses.init_pair(i, CURSES_COLORS[additive_colors[1]],
                                 CURSES_COLORS[additive_colors[1]])
        elif len(additive_colors) == 3:
            for i in range(1, 4):
                curses.init_pair(i, CURSES_COLORS[additive_colors[0]],
                                 CURSES_COLORS[additive_colors[0]])
            for i in range(4, 7):
                curses.init_pair(i, CURSES_COLORS[additive_colors[1]],
                                 CURSES_COLORS[additive_colors[1]])
            for i in range(7, 9):
                curses.init_pair(i, CURSES_COLORS[additive_colors[2]],
                                 CURSES_COLORS[additive_colors[2]])
        elif len(additive_colors) == 4:
            for i in range(1, 3):
                curses.init_pair(i, CURSES_COLORS[additive_colors[0]],
                                 CURSES_COLORS[additive_colors[0]])
            for i in range(3, 5):
                curses.init_pair(i, CURSES_COLORS[additive_colors[1]],
                                 CURSES_COLORS[additive_colors[1]])
            for i in range(5, 7):
                curses.init_pair(i, CURSES_COLORS[additive_colors[2]],
                                 CURSES_COLORS[additive_colors[2]])
            for i in range(7, 9):
                curses.init_pair(i, CURSES_COLORS[additive_colors[3]],
                                 CURSES_COLORS[additive_colors[3]])
        elif len(additive_colors) == 5:
            curses.init_pair(1, CURSES_COLORS[additive_colors[0]],
                             CURSES_COLORS[additive_colors[0]])
            for i in range(2, 4):
                curses.init_pair(i, CURSES_COLORS[additive_colors[1]],
                                 CURSES_COLORS[additive_colors[1]])
            for i in range(4, 6):
                curses.init_pair(i, CURSES_COLORS[additive_colors[2]],
                                 CURSES_COLORS[additive_colors[2]])
            for i in range(6, 8):
                curses.init_pair(i, CURSES_COLORS[additive_colors[3]],
                                 CURSES_COLORS[additive_colors[3]])
            curses.init_pair(8, CURSES_COLORS[additive_colors[4]],
                             CURSES_COLORS[additive_colors[4]])
        elif len(additive_colors) == 6:
            for i, color in enumerate(additive_colors[0:2]):
                curses.init_pair(i + 1, CURSES_COLORS[color],
                                 CURSES_COLORS[color])
            for i in range(3, 5):
                curses.init_pair(i, CURSES_COLORS[additive_colors[2]],
                                 CURSES_COLORS[additive_colors[2]])
            for i in range(5, 6):
                curses.init_pair(i, CURSES_COLORS[additive_colors[3]],
                                 CURSES_COLORS[additive_colors[3]])
            for i in range(6, 8):
                curses.init_pair(i, CURSES_COLORS[additive_colors[4]],
                                 CURSES_COLORS[additive_colors[4]])
            curses.init_pair(8, CURSES_COLORS[additive_colors[5]],
                             CURSES_COLORS[additive_colors[5]])
        elif len(additive_colors) == 7:
            for i, color in enumerate(additive_colors[0:2]):
                curses.init_pair(i + 1, CURSES_COLORS[color],
                                 CURSES_COLORS[color])
            for i in range(3, 5):
                curses.init_pair(i, CURSES_COLORS[additive_colors[2]],
                                 CURSES_COLORS[additive_colors[2]])
            for i, color in enumerate(additive_colors[3:], start=5):
                curses.init_pair(i, CURSES_COLORS[color],
                                 CURSES_COLORS[color])
        elif len(additive_colors) == 8:
            for i, color in enumerate(additive_colors):
                curses.init_pair(i + 1, CURSES_COLORS[color],
                                 CURSES_COLORS[color])
    else:
        for i in range(1, 9):
            curses.init_pair(i, CURSES_COLORS[mode], CURSES_COLORS[mode])


def static(screen, color_mode: str, args: argparse.Namespace):
    """ Main curses window. """
    set_curses_colors(color_mode, [])
    delay_time = convert_delay_number_to_delay_time(args.delay)
    color_count = cycle_count = 0
    cycle_colors = args.cycle_colors
    cycle_delay = 3
    if args.additive:
        additive_colors = ["black"]
        set_curses_colors("additive", additive_colors)
        additive_mode = True
    else:
        additive_mode = False
        additive_colors = []

    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().

    size_y, size_x = screen.getmaxyx()
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=args.run_timer)
    while True:
        if curses.is_term_resized(size_y, size_x):
            size_y, size_x = screen.getmaxyx()
            screen.clear()
            screen.refresh()
        if cycle_colors:
            color_num = list(CURSES_COLORS.keys())
            set_curses_colors(color_num[color_count], [])

        for y in range(size_y):
            for x in range(size_x):
                rand = randint(1, 20)
                block = "0" if args.test_mode else choice(block_list)
                try:
                    if rand <= 10:
                        pass  # black
                    elif rand <= 15:
                        bold = curses.color_pair(randint(1, 8)) + curses.A_BOLD
                        screen.addstr(y, x, block, bold)
                    else:
                        normal = curses.color_pair(randint(1, 8))
                        screen.addstr(y, x, block, normal)
                except curses.error:  # catching last block written off screen
                    pass
        screen.refresh()
        if cycle_count >= 10 * (cycle_delay * 5 - 4):
            color_count = 0 if color_count == 7 else color_count + 1
            cycle_count = 1
        else:
            cycle_count += 1
        ch = screen.getch()
        if args.run_timer and datetime.datetime.now() >= end_time:
            break
        if args.screen_saver and ch != -1:
            break
        elif ch in [81, 113]:  # q, Q
            break
        elif ch == 98:  # b
            set_curses_colors("bw", [])
            cycle_colors = False
            additive_mode = False
        elif ch == 67:  # C
            set_curses_colors("color", [])
            cycle_colors = False
            additive_mode = False
        elif ch == 99:  # c
            cycle_colors = True
            additive_mode = False
        elif ch == 100 or ch == 68:  # d, D
            cycle_colors = False
            set_curses_colors("color", [])
            delay_time = convert_delay_number_to_delay_time(4)
            additive_mode = False
        elif ch == 97:  # a
            if additive_mode:
                additive_mode = False
                set_curses_colors("color", [])
            else:
                cycle_colors = False
                additive_mode = True
                additive_colors = ["black"]
                set_curses_colors("additive", additive_colors)
        elif ch in curses_ch_codes_color.keys() and additive_mode:
            color = curses_ch_codes_color[ch]
            if color in additive_colors:
                additive_colors.pop(additive_colors.index(color))
            else:
                additive_colors.append(color)
            set_curses_colors("additive", additive_colors)
        elif ch in curses_ch_codes_color.keys():
            color = curses_ch_codes_color[ch]
            set_curses_colors(color, [])
            cycle_colors = False
        elif ch in curses_number_ch_codes.keys():
            number = curses_number_ch_codes[ch]
            delay_time = convert_delay_number_to_delay_time(number)
        elif ch in curses_shift_num_codes.keys():
            cycle_delay = curses_shift_num_codes[ch]
        sleep(delay_time)

    # clear screen before returning
    screen.clear()
    screen.refresh()


def convert_delay_number_to_delay_time(delay_num: int) -> float:
    """ Converts delay number into delay time for sleep function. """
    return round((delay_num / 100) * (0.5 + delay_num/2), 2)


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse module.
    Checks to see if value is positive int between 0 and 10.
    """
    msg = f"{value} is an invalid positive int 0 to 9"
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(msg)
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(msg)


def color_type(value: str) -> str:
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in CURSES_COLORS.keys():
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def list_commands() -> None:
    print("List of running commands:")
    print(" Q       To quit")
    print(" b       Enable black and white mode")
    print(" C       Enable color mode")
    print(" c       Enable cycle color mode")
    print(" a       Enable additive mode (r,t,y,u,i,o,p,[) "
          "to add and remove colors")
    print(" d       Reset to default settings")
    print(" 0 - 9   Delay. 0-Fast, 4-Default, 9-Slow")
    print("shift 1 - 5 Color cycle delay time. 1-Fast, 3-Default, 5-Slow")
    print(" r,t,y,u,i,o,p,[   Set single color")


def list_colors() -> None:
    print("Color List:")
    print(", ".join(CURSES_COLORS.keys()))


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """ Command line argument setup and parsing by argparse. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=4,
                        type=positive_int_zero_to_nine,
                        help="Delay setting (speed):  "
                             "0 - Fast, 4 - Default, 9 - Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode. Overrides -C")
    parser.add_argument("-C", dest="color", type=color_type, default=None,
                        metavar="COLOR", help="Set a single color to use")
    parser.add_argument("-s", dest="start_timer",
                        type=argparse_types.pos_int, default=0,
                        help="Set a start timer in seconds", metavar="SECONDS")
    parser.add_argument("-r", dest="run_timer",
                        type=argparse_types.pos_int, default=0,
                        metavar="SECONDS", help="Set a run timer in seconds")
    parser.add_argument("-S", dest="screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will quit")
    parser.add_argument("-c", dest="cycle_colors", action="store_true",
                        help="Cycle through colors")
    parser.add_argument("-a", dest="additive", action="store_true",
                        help="Additive color mode. Use color keys "
                             "(r,t,y,u,i,o,p,[) to add and remove colors")
    parser.add_argument("--list_colors", action="store_true",
                        help="List available colors and exit.")
    parser.add_argument("--list_commands", action="store_true",
                        help="List running commands.")
    parser.add_argument("--version", action="version", version=version)
    parser.add_argument("--test_mode", action="store_true",
                        help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main() -> int:
    """ Main function. """
    args = argument_parser()
    if args.list_commands:
        list_commands()
        return 0
    elif args.list_colors:
        list_colors()
        return 0

    if args.black_white:
        color_mode = "bw"
    elif args.color:
        color_mode = args.color
    else:
        color_mode = "color"

    sleep(args.start_timer)
    try:
        curses.wrapper(static, color_mode, args)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    exit(main())
