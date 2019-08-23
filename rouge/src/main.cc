#include <iostream>
#include <cstdlib>
#include <curses.h>

#include "map.h"

using namespace std;

// TODO: Put Ellen in

int main() {
  try {
    initscr();
    raw();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);

    addch('a' | A_BOLD | A_BLINK);
    mvprintw(1, 2, "Press q to exit");

    std::unique_ptr<Map> map;
    auto err = Map::default_map(map);
    if (err != makeMapStatusOk) {
      endwin();
      return EXIT_FAILURE;
    }
    map->render();

    refresh();

    while (true) {
      char c = getch();
      switch (c) {
        case 'q':
          endwin();
          return EXIT_SUCCESS;
        default:
          break;
      }
    }
  } catch (...) {
    endwin();
    return EXIT_FAILURE;
  }
}

