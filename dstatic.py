""" Snow / static simulation using curses. """

import argparse
import curses
import datetime
import sys
from random import randint
from time import sleep

version = "0.6"

curses_number_ch_codes = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9}


def set_curses_colors():
    """ Set the color pairs in the curses module. """
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
    """ Set black and white color pairs in the curses module. """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)
    return 3


def static(screen, delay, black_white, run_timer, screen_saver_mode):
    """ Main curses window. """
    if black_white:
        number_of_pairs = set_curses_black_white()
    else:
        number_of_pairs = set_curses_colors()

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
                if rand <= 9:
                    pass
                elif rand <= 11:
                    screen.addstr(y,
                                  x,
                                  " ",
                                  curses.color_pair(randint(1, number_of_pairs)) +
                                  curses.A_STANDOUT + curses.A_BOLD)
                else:
                    screen.addstr(y,
                                  x,
                                  "1",
                                  curses.color_pair(randint(1, number_of_pairs)))
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
                number_of_pairs = set_curses_black_white()
            elif ch == 99:  # c
                number_of_pairs = set_curses_colors()
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


def list_commands():
    print("List of running commands:")
    print(" Q     To quit")
    print(" b     Enable black and white mode")
    print(" c     Enable color mode")
    print(" 0 - 9 Delay. 0-Fast, 4-Default, 9-Slow")


def argument_parsing(argv):
    """ Command line argument setup and parsing by argparse. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=4, type=positive_int_zero_to_nine,
                        help="Delay setting (speed):  0 - Fast, 4 - Default, 9 - Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode")
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

    sleep(args.start_timer)
    delay_time = convert_delay_number_to_delay_time(args.delay)
    # print("dstatic")
    try:
        curses.wrapper(static, delay_time, args.black_white,
                       args.run_timer, args.screen_saver)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    main()
