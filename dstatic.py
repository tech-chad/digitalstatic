""" Snow / static simulation using curses. """

import argparse
import curses
import sys
from time import sleep
from random import randint

version = "0.3"


def set_curses_colors():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_CYAN)
    return 8


def set_curses_black_white():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)
    return 3


def static(screen, delay, black_white):
    if black_white:
        number_of_pairs = set_curses_black_white()
    else:
        number_of_pairs = set_curses_colors()

    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().

    size_y, size_x = screen.getmaxyx()
    while True:
        resize = curses.is_term_resized(size_y, size_x)
        if resize is True:
            screen.clear()
            screen.refresh()

        size_y, size_x = screen.getmaxyx()
        for y in range(size_y - 1):
            for x in range(size_x):
                rand = randint(1, 20)
                if rand <= 9:
                    pass
                elif rand <= 11:
                    screen.addstr(y, x, " ", curses.color_pair(randint(1, number_of_pairs)) +
                                  curses.A_STANDOUT + curses.A_BOLD)
                else:
                    screen.addstr(y, x, " ", curses.color_pair(randint(1, number_of_pairs)))
        screen.refresh()

        ch = screen.getch()
        if ch in [81, 113]:
            screen.clear()
            screen.refresh()
            break
        sleep(delay)


def delay_positive_int(value):
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return round((int_value / 100) * (0.5 + int_value/2), 2)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")


# For use with arg parse to check to see if value is positive int.
def positive_int(value):
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return int_value


def argument_parsing(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=0.1, type=delay_positive_int,
                        help="Delay setting (speed):  0 - Fast, 4 - Default, 9 - Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode")
    parser.add_argument("-s", dest="start_timer", type=positive_int, default=0,
                        help="Set a start timer in seconds", metavar="SECONDS")
    return parser.parse_args(argv)


def main():
    args = argument_parsing(sys.argv[1:])
    sleep(args.start_timer)
    curses.wrapper(static, args.delay, args.black_white)


if __name__ == "__main__":
    main()
