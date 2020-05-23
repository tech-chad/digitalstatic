#! /usr/bin/python3
""" Snow / static simulation using curses. """

import argparse
import curses
import datetime
import sys
from random import randint, choice
from time import sleep

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

version = importlib_metadata.version("digital_static")

curses_number_ch_codes = {48: 0, 49: 1, 50: 2, 51: 3, 52:
                          4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9}
color_list = ["red", "green", "blue", "yellow", "magenta", "cyan", "black", "white"]
curses_ch_codes_color = {114: "red", 116: "green", 121: "blue", 117: "yellow",
                         105: "magenta", 111: "cyan", 112: "white", 91: "black"}
block_list = [chr(9617), chr(9618), chr(9619), chr(9608), " "]


def set_curses_colors() -> None:
    """ Set curses colors. """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_CYAN)


def static(screen, color_mode: str, argv: argparse.Namespace):
    """ Main curses window. """
    color_pair_dict = {"blue": [3, 3], "green": [4, 4], "magenta": [5, 5],
                       "yellow": [6, 6], "red": [7, 7], "cyan": [8, 8],
                       "bw": [1, 1, 2], "black": [1, 1],
                       "color": [1, 2, 3, 4, 5, 6, 7, 8], "white": [2, 2]}
    set_curses_colors()
    current_color_pair_list = color_pair_dict[color_mode]
    delay_time = convert_delay_number_to_delay_time(argv.delay)
    color_count = cycle_count = 1
    cycle_colors = argv.cycle_colors

    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().

    size_y, size_x = screen.getmaxyx()
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=argv.run_timer)
    while True:
        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            screen.clear()
            screen.refresh()

        size_y, size_x = screen.getmaxyx()
        for y in range(size_y - 1):
            for x in range(size_x):
                rand = randint(1, 20)
                if cycle_colors:
                    pair_num = color_count
                    if cycle_count >= 200000:
                        color_count = 1 if color_count == 8 else color_count + 1
                        cycle_count = 1
                    else:
                        cycle_count += 1
                else:
                    pair_num = choice(current_color_pair_list)
                if argv.test_mode:
                    block = "0"
                else:
                    block = choice(block_list)
                normal = curses.color_pair(pair_num)
                bold = curses.color_pair(pair_num) + curses.A_BOLD
                if rand <= 10:
                    pass  # black
                elif rand <= 15:
                    screen.addstr(y, x, block, bold)
                else:
                    screen.addstr(y, x, block, normal)
        screen.refresh()

        ch = screen.getch()
        # print(ch, file=open("debug.txt", "w"))  # not sure what used for ??
        if argv.run_timer and datetime.datetime.now() >= end_time:
            break
        if argv.screen_saver and ch != -1:
            break
        elif ch != -1:
            if ch in [81, 113]:  # q, Q
                break
            elif ch == 98:  # b
                current_color_pair_list = color_pair_dict["bw"]
                cycle_colors = False
            elif ch == 67:  # C
                current_color_pair_list = color_pair_dict["color"]
                cycle_colors = False
            elif ch == 99:  # c
                cycle_colors = True
            elif ch == 100 or ch == 68:  # d, D
                cycle_colors = False
                current_color_pair_list = color_pair_dict["color"]
                delay_time = convert_delay_number_to_delay_time(4)
            elif ch in curses_ch_codes_color.keys():
                color = curses_ch_codes_color[ch]
                current_color_pair_list = color_pair_dict[color]
            elif ch in curses_number_ch_codes.keys():
                number = curses_number_ch_codes[ch]
                delay_time = convert_delay_number_to_delay_time(number)
        sleep(delay_time)

    # clear screen before returning
    screen.clear()
    screen.refresh()


def convert_delay_number_to_delay_time(delay_num: int) -> float:
    return round((delay_num / 100) * (0.5 + delay_num/2), 2)


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse module.
    Checks to see if value is positive int between 0 and 10.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int 0 to 9")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int 0 to 9")


def positive_int(value: str) -> int:
    """
    Used by argparse module.
    Checks to see if the value is positive.
    """
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return int_value


def color_type(value: str) -> str:
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in color_list:
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def list_commands() -> None:
    print("List of running commands:")
    print(" Q       To quit")
    print(" b       Enable black and white mode")
    print(" C       Enable color mode")
    print(" c       Enable cycle color mode")
    print(" d       Reset to default settings")
    print(" 0 - 9   Delay. 0-Fast, 4-Default, 9-Slow")
    print(" r,t,y,u,i,o,p,[   Set single color")


def list_colors() -> None:
    print("Color List:")
    print(", ".join(color_list))


def argument_parsing(argv: list) -> argparse.Namespace:
    """ Command line argument setup and parsing by argparse. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=4, type=positive_int_zero_to_nine,
                        help="Delay setting (speed):  0 - Fast, 4 - Default, 9 - Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode. Overrides -C")
    parser.add_argument("-C", dest="color", type=color_type, default=None,
                        metavar="COLOR", help="Set a single color to use")
    parser.add_argument("-s", dest="start_timer", type=positive_int, default=0,
                        help="Set a start timer in seconds", metavar="SECONDS")
    parser.add_argument("-r", dest="run_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set a run timer in seconds")
    parser.add_argument("-S", dest="screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will quit")
    parser.add_argument("-c", dest="cycle_colors", action="store_true",
                        help="Cycle through colors")
    parser.add_argument("--list_colors", action="store_true",
                        help="List available colors and exit.")
    parser.add_argument("--list_commands", action="store_true",
                        help="List running commands.")
    parser.add_argument("--test_mode", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main() -> int:
    """ Main function. """
    args = argument_parsing(sys.argv[1:])
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
    main()
