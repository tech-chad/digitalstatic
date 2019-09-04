""" Snow / static simulation using curses. """

import curses
from time import sleep
from random import randint

version = "0.1"


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


def static(screen):
    number_of_pairs = set_curses_colors()
    curses.curs_set(0)  # Set the cursor to off.

    size_y, size_x = screen.getmaxyx()

    screen.timeout(0)  # Turn blocking off for screen.getch().
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
        sleep(0.09)


def main():
    curses.wrapper(static)


if __name__ == "__main__":
    main()
