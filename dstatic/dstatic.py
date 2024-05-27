""" Snow / static simulation using curses. """
import argparse
import curses
import datetime
import random
import sys
import time

from typing import List
from typing import Optional
from typing import Sequence

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

VERSION = importlib_metadata.version("digital_static")

COLORS = {
    "all": [16, 255, 160, 40, 21, 184, 164, 44, 124, 22, 17],
    "B&W": [16, 232, 233, 234, 235, 236, 237, 238, 240, 241,
            242, 244, 245, 246, 247, 248, 249, 250, 252, 255],
    "red": [52, 88, 124, 160, 196, 197, 160, 124, 160],
    "green": [22, 28, 34, 40, 46, 76, 40, 40, 22, 40],
    "blue": [17, 19, 20, 21, 26, 63, 21, 21, 17, 21],
    "yellow": [58, 94, 100, 106, 178, 184, 184, 184, 100],
    "cyan": [23, 30, 31, 44, 45, 51, 44, 44, 31],
    "magenta": [53, 91, 127, 126, 164, 201, 164, 164, 126],
    "all 8": [0, 1, 2, 3, 4, 5, 6, 7],
    "B&W 8": [0, 7, 0, 7, 0, 7, 0, 7],
    "red 8": [1, 1, 1, 1, 1, 7, 0, ],
    "green 8": [2, 2, 2, 2, 2, 7, 0, ],
    "blue 8": [4, 4, 4, 4, 4, 7, 0, ],
    "yellow 8": [3, 3, 3, 3, 3, 7, 0, ],
    "cyan 8": [6, 6, 6, 6, 6, 7, 0, ],
    "magenta 8": [5, 5, 5, 5, 5, 7, 0, ],
}
LIST_OF_COLORS = ["red", "green", "blue", "yellow", "cyan", "magenta", "B&W"]
DELAY_SPEED = [0.01, 0.04, 0.05, 0.06, 0.07, 0.09, 0.11, 0.15, 0.2, 0.4]
DEFAULT_SPEED = 4
CYCLE_COLOR_SPEED = [30, 80, 120, 160, 250]
CURSES_NUM_SHIFT_CODES = {33: 1, 64: 2, 35: 3, 36: 4, 37: 5}
CURSES_CODES_COLORS = {114: "red", 116: "green", 121: "blue", 117: "yellow",
                       105: "magenta", 111: "cyan"}
NUMBER_OF_TEST_PATTERNS = 3


def setup_curses_colors(color: str) -> int:
    # return the number of color pair init
    if curses.COLORS < 256:
        color = color + " 8"
    color_number_list = COLORS[color]
    [curses.init_pair(i + 1, color_number, color_number)
     for i, color_number in enumerate(color_number_list)]
    return len(color_number_list)


def setup_curses_colors_additive(color_list: List[str]) -> int:
    # return the number of color pair init
    color_list_numbers = []
    for color in color_list:
        if curses.COLORS < 256:
            color = color + " 8"
        color_list_numbers.extend(COLORS[color])
    [curses.init_pair(i + 1, color_number, color_number)
     for i, color_number in enumerate(color_list_numbers)]
    return len(color_list_numbers)


def display_test_pattern1(screen, size_y: int, size_x: int,
                          test_mode: bool) -> None:
    color_names = {curses.COLOR_WHITE: "w", curses.COLOR_YELLOW: "y",
                   curses.COLOR_CYAN: "c", curses.COLOR_GREEN: "g",
                   curses.COLOR_MAGENTA: "m", curses.COLOR_RED: "r",
                   curses.COLOR_BLUE: "b", curses.COLOR_BLACK: "B"}
    screen.erase()
    split_x = size_x // 8
    colors = [curses.COLOR_WHITE, curses.COLOR_YELLOW, curses.COLOR_CYAN,
              curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED,
              curses.COLOR_BLUE, curses.COLOR_BLACK]
    for i, c in enumerate(colors, start=1):
        curses.init_pair(i, c, c)
    for i in range(1, 9):
        ch = color_names[colors[i - 1]] if test_mode else " "
        for y in range(size_y - 1):
            for x in range(split_x * (i - 1), split_x * i):
                screen.addstr(y, x, ch, curses.color_pair(i))
    screen.refresh()


def display_test_pattern2(screen, size_y: int, size_x: int,
                          test_mode: bool) -> None:
    color_names = {curses.COLOR_WHITE: "w", curses.COLOR_YELLOW: "y",
                   curses.COLOR_CYAN: "c", curses.COLOR_GREEN: "g",
                   curses.COLOR_MAGENTA: "m", curses.COLOR_RED: "r",
                   curses.COLOR_BLUE: "b", curses.COLOR_BLACK: "B"}
    colors = [curses.COLOR_WHITE, curses.COLOR_YELLOW, curses.COLOR_CYAN,
              curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED,
              curses.COLOR_BLUE, curses.COLOR_BLACK]
    for i, c in enumerate(colors, start=1):
        curses.init_pair(i, c, c)
    split_x = size_x // 7
    split_y = size_y // 10
    screen.erase()
    for i in range(1, 8):
        ch = color_names[colors[i - 1]] if test_mode else " "
        for y in range(size_y - split_y):
            for x in range(split_x * (i - 1), split_x * i):
                screen.addstr(y, x, ch, curses.color_pair(i))
    for i in range(1, 8):
        ch = color_names[colors[9 - i - 1]] if test_mode else " "
        for y in range(size_y - split_y, size_y - 1):
            for x in range(split_x * (i - 1), split_x * i):
                screen.addstr(y, x, ch, curses.color_pair(9 - i) + curses.A_BOLD)
    screen.refresh()


def display_test_pattern3(screen, size_y: int, size_x: int,
                          test_mode: bool) -> None:
    color_names = {curses.COLOR_WHITE: "w", curses.COLOR_YELLOW: "y",
                   curses.COLOR_CYAN: "c", curses.COLOR_GREEN: "g",
                   curses.COLOR_MAGENTA: "m", curses.COLOR_RED: "r",
                   curses.COLOR_BLUE: "b", curses.COLOR_BLACK: "B",
                   17: "n"}
    if curses.COLORS < 256:
        colors = [curses.COLOR_WHITE, curses.COLOR_YELLOW, curses.COLOR_CYAN,
                  curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED,
                  curses.COLOR_BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE]
    else:
        colors = [curses.COLOR_WHITE, curses.COLOR_YELLOW, curses.COLOR_CYAN,
                  curses.COLOR_GREEN, curses.COLOR_MAGENTA, curses.COLOR_RED,
                  curses.COLOR_BLUE, curses.COLOR_BLACK, 17]
    for i, c in enumerate(colors, start=1):
        curses.init_pair(i, c, c)
    split_x = size_x // 7
    split_y = size_y // 10
    screen.erase()
    for i in range(1, 8):
        ch = color_names[colors[i - 1]] if test_mode else " "
        for y in range(size_y - split_y * 4):
            for x in range(split_x * (i - 1), split_x * i):
                screen.addstr(y, x, ch, curses.color_pair(i))
    for i in range(1, 8):
        ch = color_names[colors[i - 1]] if test_mode else " "
        for y in range(size_y - split_y * 4, size_y - split_y * 3):
            for x in range(split_x * (i - 1), split_x * i):
                screen.addstr(y, x, ch, curses.color_pair(9 - i) + curses.A_BOLD)
    split_x = size_x // 6
    ch = color_names[colors[8]] if test_mode else " "
    for y in range(size_y - split_y * 3, size_y - 1):
        for x in range(0, split_x + 5):
            screen.addstr(y, x, ch, curses.color_pair(9))
    ch = color_names[colors[0]] if test_mode else " "
    for y in range(size_y - split_y * 3, size_y - 1):
        for x in range(split_x + 5, split_x * 2):
            screen.addstr(y, x, ch, curses.color_pair(1) + curses.A_BOLD)
    ch = color_names[colors[8]] if test_mode else " "
    for y in range(size_y - split_y * 3, size_y - 1):
        for x in range(split_x * 2, split_x * 3 + 5):
            screen.addstr(y, x, ch, curses.color_pair(9))
    screen.refresh()


def blue_screen_display(screen, size_y: int, size_x: int) -> None:
    text = """

  A problem has been detected and windows has been shut down to prevent damage
  to your computer.

  PFN_LIST_CORRUPT

  If this is the first time you've seen this Stop error screen,
  restart your computer. If this screen appears again, follow
  theses steps:

  Check to make sure any new hardware or software is properly installed.
  If this is a new installation, ask your hardware or software manufacturer
  for any windows updates you might need.

  If problems continue, disable or remove any newly installed hardware
  or software. Disable BIOS memory options such as caching or shadowing.
  If you need to use Safe Mode to remove or disable components, restart
  your computer, press F8 to select Advance Startup Options, and then
  select Safe Mode.

  Technical information:
  *** STOP: 0x0000004e (0x00000099, 0x00900009, 0x00000900, 0x00000900)
"""
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    screen.erase()
    text_list = text.splitlines()
    for y in range(size_y):
        if y < len(text_list):
            screen.addstr(y, 0, text_list[y], curses.color_pair(1))
            start_x = len(text_list[y])
        else:
            start_x = 0
        for x in range(start_x, size_x):
            try:
                screen.addstr(y, x, " ", curses.color_pair(1))
            except curses.error:
                pass
    screen.refresh()


def static(screen, args: argparse.Namespace) -> None:
    """ Main curses window. """
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    curses.use_default_colors()
    cycle_color = cycle_time = 0
    cycle_change = CYCLE_COLOR_SPEED[3]
    additive_list = ["B&W"]
    test_pattern = 0
    blue_screen = 0
    if args.black_white:
        color_name = "B&W"
        num_of_pairs = setup_curses_colors(color_name)
    elif args.color is not None:
        color_name = args.color
        num_of_pairs = setup_curses_colors(color_name)
    elif args.cycle_color_mode:
        color_name = LIST_OF_COLORS[cycle_color]
        num_of_pairs = setup_curses_colors(color_name)
    elif args.additive:
        color_name = "Add"
        num_of_pairs = setup_curses_colors_additive(additive_list)
    else:
        color_name = "all"
        num_of_pairs = setup_curses_colors(color_name)
    color_changed = False
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=args.run_timer)
    size_y, size_x = screen.getmaxyx()
    run = True
    while run:
        if curses.is_term_resized(size_y, size_x):
            size_y, size_x = screen.getmaxyx()
            if test_pattern:
                screen.erase()
                screen.refresh()
        if args.test_mode:
            char = color_name[0]
            cycle_change = 3
        else:
            char = " "
        if test_pattern:
            size_y, size_x = screen.getmaxyx()
            if test_pattern == 1:
                display_test_pattern1(screen, size_y, size_x, args.test_mode)
            elif test_pattern == 2:
                display_test_pattern2(screen, size_y, size_x, args.test_mode)
            elif test_pattern == 3:
                display_test_pattern3(screen, size_y, size_x, args.test_mode)
        elif blue_screen:
            size_y, size_x = screen.getmaxyx()
            blue_screen_display(screen, size_y, size_x)
        else:
            if color_changed:
                [screen.addstr(y, x, char,
                               curses.color_pair(random.randint(1, num_of_pairs)))
                 for y in range(size_y) for x in range(size_x - 1)]
            else:
                [screen.addstr(
                    random.randint(0, size_y - 1),
                    random.randint(0, size_x - 2),
                    char,
                    curses.color_pair(random.randint(1, num_of_pairs)))
                 for _ in range((size_y * (size_x - 1)) - 15)]
        screen.refresh()
        time.sleep(DELAY_SPEED[args.delay])
        if args.run_timer and datetime.datetime.now() >= end_time:
            break
        color_changed = False
        if args.cycle_color_mode and cycle_time >= cycle_change:
            if cycle_color == len(LIST_OF_COLORS) - 1:
                cycle_color = 0
            else:
                cycle_color += 1
            color_name = LIST_OF_COLORS[cycle_color]
            num_of_pairs = setup_curses_colors(color_name)
            color_changed = True
            cycle_time = 0
        else:
            cycle_time += 1
        ch = screen.getch()
        if ch == curses.KEY_RESIZE:
            size_y, size_x = screen.getmaxyx()
            color_changed = True
        if ch == -1:
            continue
        if args.screen_saver and ch != -1:
            run = False
        elif args.disable_all_keys:
            continue
        elif ch in [81, 113]:  # q Q
            run = False
        elif args.disable_keys:
            continue
        elif ch == 98:  # b
            color_name = "all" if color_name == "B&W" else "B&W"
            num_of_pairs = setup_curses_colors(color_name)
            color_changed = True
            args.cycle_color_mode = False
            args.additive = False
        elif ch == 67:  # C
            color_name = "all"
            num_of_pairs = setup_curses_colors(color_name)
            color_changed = True
            args.additive = False
            args.cycle_color_mode = False
        elif ch in [100, 68]:  # d or D
            color_name = "all"
            num_of_pairs = setup_curses_colors(color_name)
            test_pattern = 0
            color_changed = True
            args.delay = DEFAULT_SPEED
            args.cycle_color_mode = False
            cycle_change = CYCLE_COLOR_SPEED[3]
            args.additive = False
        elif 48 <= ch <= 57:  # number keys 1 to 0
            args.delay = int(chr(ch))
        elif ch in [114, 116, 121, 117, 105, 111] and args.additive:
            c = CURSES_CODES_COLORS[ch]
            if c in additive_list:
                additive_list.pop(additive_list.index(c))
            else:
                additive_list.append(c)
            num_of_pairs = setup_curses_colors_additive(additive_list)
            color_changed = True
        elif ch in [114, 116, 121, 117, 105, 111]:  # r, t, y, u, i, o
            color_name = CURSES_CODES_COLORS[ch]
            num_of_pairs = setup_curses_colors(color_name)
            color_changed = True
            args.cycle_color_mode = False
            args.additive = False
        elif ch == 99:  # c
            if args.cycle_color_mode:
                args.cycle_color_mode = False
                color_name = "all"
                num_of_pairs = setup_curses_colors(color_name)
                color_changed = True
                cycle_change = CYCLE_COLOR_SPEED[3]
            else:
                args.cycle_color_mode = True
                cycle_color = cycle_time = 0
                color_name = LIST_OF_COLORS[cycle_color]
                num_of_pairs = setup_curses_colors(color_name)
                color_changed = True
                args.additive = False
        elif ch in [33, 64, 35, 36, 37] and args.cycle_color_mode:
            cycle_change = CYCLE_COLOR_SPEED[CURSES_NUM_SHIFT_CODES[ch] - 1]
        elif ch == 97:  # a
            if args.additive:
                args.additive = False
                color_name = "all"
                num_of_pairs = setup_curses_colors(color_name)
                color_changed = True
            else:
                color_name = "Add"
                args.additive = True
                args.cycle_color_mode = False
                additive_list = ["B&W"]
                num_of_pairs = setup_curses_colors_additive(additive_list)
                color_changed = True
        elif ch == 108:  # l
            screen.erase()
            screen.refresh()
            time.sleep(2)
        elif ch == 122:  # z
            if test_pattern == NUMBER_OF_TEST_PATTERNS:
                test_pattern = 0
                num_of_pairs = setup_curses_colors(color_name)
            else:
                test_pattern += 1
        elif ch == 119:  # w
            if blue_screen == 1:
                blue_screen = 0
                screen.erase()
                screen.refresh()
                num_of_pairs = setup_curses_colors(color_name)
            else:
                blue_screen += 1

        elif ch == 102:  # f
            while True:
                ch = screen.getch()
                if ch == 102:
                    break
    # clear the screen before exit
    screen.erase()
    screen.refresh()


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
    if lower_value in LIST_OF_COLORS:
        return lower_value
    raise argparse.ArgumentTypeError(f"{value} is an invalid color name")


def pos_int(value: str) -> int:
    """ Used with argparse.  Positive int value not including 0"""
    error_msg = f"{value} is an invalid positive int value"
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(error_msg)
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            return int_value


def list_commands() -> None:
    print("List of running commands:")
    print(" Q or q           To quit")
    print(" b                Toggle black and white mode")
    print(" C                Enable color mode (default mode)")
    print(" c                Toggle cycle color mode")
    print(" a                Toggle additive mode (r,t,y,u,i,o) "
          "to add and remove colors")
    print(" d                Reset to default settings")
    print(f" 0 - 9            Delay. 0-Fast, {DEFAULT_SPEED}-Default, 9-Slow")
    print(" shift 1 - 5      Color cycle time. 1-Fast, 3-Default, 5-Slow")
    print(" r,t,y,u,i,o,p,[  Set single color")
    print(" f                Freeze screen until 'f' is pressed again.")
    print(" l                Clear the screen wait 2 seconds and start again")
    print(" z                Cycle through test patterns. Total test"
          f" patterns {NUMBER_OF_TEST_PATTERNS}")
    print(" w                Display fake blue screen of death")


def list_colors() -> None:
    print("Color List:")
    print(", ".join(LIST_OF_COLORS[0:-1]))


def argument_parser(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """ Command line argument setup and parsing by argparse. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="delay", default=DEFAULT_SPEED,
                        type=positive_int_zero_to_nine,
                        help="Delay setting (speed):  "
                             f"0-Fast, {DEFAULT_SPEED}-Default, 9-Slow")
    parser.add_argument("-b", dest="black_white", action="store_true",
                        help="Enable black and white mode. Overrides -C")
    parser.add_argument("-C", "--color", type=color_type, default=None,
                        metavar="COLOR", help="Set a single color to use")
    parser.add_argument("-s", "--start_timer", type=pos_int, default=0,
                        help="Set a start timer in seconds", metavar="SECONDS")
    parser.add_argument("-r", "--run_timer",
                        type=pos_int, default=0,
                        metavar="SECONDS", help="Set a run timer in seconds")
    parser.add_argument("-S", "--screen_saver", action="store_true",
                        help="Screen saver mode.  Any key will quit")
    parser.add_argument("-c", "--cycle_colors", dest="cycle_color_mode",
                        action="store_true", help="Cycle through colors")
    parser.add_argument("-a", "--additive", action="store_true",
                        help="Additive color mode. Use color keys "
                             "(r,t,y,u,i,o) to add and remove colors")
    parser.add_argument("-D", "--disable_keys", action="store_true",
                        help="Disable keys while running except for 'Q' or "
                             "'q' and for ctrl-c. Does not affect screensaver"
                             "mode.")
    parser.add_argument("--disable_all_keys", action="store_true",
                        help="Disable all keys while running including "
                             "'Q' and 'q.'"
                        "Use ctrl-c to quit. Does not affect screensaver mode.")
    parser.add_argument("--list_colors", action="store_true",
                        help="List available colors and exit.")
    parser.add_argument("--list_commands", action="store_true",
                        help="List running commands and exit.")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--test_mode", action="store_true",
                        help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = argument_parser(argv)
    if args.list_commands:
        list_commands()
        return 0
    elif args.list_colors:
        list_colors()
        return 0

    time.sleep(args.start_timer)
    try:
        curses.wrapper(static, args)
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    exit(main())
