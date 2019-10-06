""" Snow / static simulation using curses. """

import argparse
import curses
import datetime
import sys
from random import randint, choice
from time import sleep

version = "0.6"

curses_number_ch_codes = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9}
color_list = ["red", "green", "blue", "yellow", "magenta", "cyan", "black", "white"]
curses_ch_codes_color = {114: "red", 116: "green", 121: "blue", 117: "yellow",
                         105: "magenta", 111: "cyan", 112: "white", 91: "black"}


def set_curses_colors():
    """ Set curses colors. """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_CYAN)


def static(screen, delay, color_mode, run_timer, screen_saver_mode):
    """ Main curses window. """
    color_pair_dict = {"blue": [3, 3], "green": [4, 4], "magenta": [5, 5], "yellow": [6, 6],
                       "red": [7, 7], "cyan": [8, 8], "bw": [1, 1, 2], "black": [1, 1],
                       "color": [1, 2, 3, 4, 5, 6, 7, 8], "white": [2, 2]}
    set_curses_colors()
    current_color_pair_list = color_pair_dict[color_mode]

    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().

    size_y, size_x = screen.getmaxyx()
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=run_timer)
    while True:
        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            screen.clear()
            screen.refresh()

        size_y, size_x = screen.getmaxyx()
        for y in range(size_y - 1):
            for x in range(size_x):
                rand = randint(1, 20)
                pair_num = choice(current_color_pair_list)
                if rand <= 10:
                    pass
                elif rand <= 15:
                    color_effect = curses.A_STANDOUT + curses.A_BOLD
                    screen.addstr(y, x, " ", curses.color_pair(pair_num) + color_effect)
                else:
                    screen.addstr(y, x, "1", curses.color_pair(pair_num))
        screen.refresh()

        ch = screen.getch()
        print(ch, file=open("debug.txt", "w"))
        if run_timer and datetime.datetime.now() >= end_time:
            screen.clear()
            screen.refresh()
            break
        if screen_saver_mode and ch != -1:
            screen.clear()
            screen.refresh()
            break
        elif ch != -1:
            if ch in [81, 113]:
                screen.clear()
                screen.refresh()
                break
            elif ch == 98:  # b
                current_color_pair_list = color_pair_dict["bw"]
            elif ch == 99:  # c
                current_color_pair_list = color_pair_dict["color"]
            elif ch in curses_ch_codes_color.keys():
                color = curses_ch_codes_color[ch]
                current_color_pair_list = color_pair_dict[color]
            elif ch in curses_number_ch_codes.keys():
                number = curses_number_ch_codes[ch]
                delay = convert_delay_number_to_delay_time(number)
        sleep(delay)


def convert_delay_number_to_delay_time(delay_num):
    return round((delay_num / 100) * (0.5 + delay_num/2), 2)


def positive_int_zero_to_nine(value):
    """
    Used with argparse module.
    Checks to see if value is positive int between 0 and 10.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive "
                                             f"int value 0 to 9")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int "
                                         f"value 0 to 9")


def positive_int(value):
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


def color_type(value):
    """
    Used with argparse
    Checks to see if the value is a valid color and returns
    the lower case color name.
    """
    lower_value = value.lower()
    if lower_value in color_list:
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def list_commands():
    print("List of running commands:")
    print(" Q       To quit")
    print(" b       Enable black and white mode")
    print(" c       Enable color mode")
    print(" 0 - 9   Delay. 0-Fast, 4-Default, 9-Slow")
    print(" r,t,y,u,i,o,p,[   Set single color")


def argument_parsing(argv):
    """ Command line argument setup and parsing by argparse. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=4, type=positive_int_zero_to_nine,
                        help="Delay setting (speed):  0 - Fast, 4 - Default, 9 - Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode. Overrides -C")
    parser.add_argument("-C", dest="color", type=color_type, default=None, metavar="COLOR",
                        help="Set a single color to use")
    parser.add_argument("-s", dest="start_timer", type=positive_int, default=0,
                        help="Set a start timer in seconds", metavar="SECONDS")
    parser.add_argument("-r", dest="run_timer", type=positive_int, default=0,
                        metavar="SECONDS", help="Set a run timer in seconds")
    parser.add_argument("-S", dest="screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will quit")
    parser.add_argument("--list_commands", action="store_true",
                        help="List running commands.")
    return parser.parse_args(argv)


def main():
    """ Main function. """
    args = argument_parsing(sys.argv[1:])
    if args.list_commands:
        list_commands()
        return

    if args.black_white:
        color_mode = "bw"
    elif args.color:
        color_mode = args.color
    else:
        color_mode = "color"

    sleep(args.start_timer)
    delay_time = convert_delay_number_to_delay_time(args.delay)
    try:
        curses.wrapper(static, delay_time, color_mode,
                       args.run_timer, args.screen_saver)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    main()
