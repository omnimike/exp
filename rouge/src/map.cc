
#include <fstream>
#include <string>
#include <stdint.h>
#include <sstream> 
#include <ncurses.h>

#include "map.h"
#include "point.h"
#include "tile.h"
#include "map_data.h"

void Map::render() {
  mvprintw(2, 2, "rendering my map!!!");
}

std::unique_ptr<Map> Map::default_map() {
  uint32_t pos = 0; 
  uint32_t rows = 0;
  uint32_t cols = 0;
  unsigned char c = src_map_data[pos];
  if (!(pos < src_map_data_len && c >= '0' && c <= '9')) {

  }
  while (pos < src_map_data_len && c >= '0' && c <= '9') {
      rows *= 10;
      rows += c;
      ++pos;
      c = src_map_data[pos];
  }
  if (c != ' ') {

  }
  ++pos;
  if (!(pos < src_map_data_len && c >= '0' && c <= '9')) {

  }
  while (pos < src_map_data_len && c >= '0' && c <= '9') {
      cols *= 10;
      cols += c;
      ++pos;
      c = src_map_data[pos];
  }
  if (c != '\n') {
    
  }
  ++pos;


  std::unique_ptr<Tile> tile;
  auto tiles(std::make_unique<std::vector<Tile>());
  uint32_t x = 0;
  uint32_t y = 0;
  Point start;
  uint32_t max_x = 0;
  for (uint32_t i = 0; i < src_map_data_len; ++i) {
    char c = src_map_data[i];
    std::unique_ptr<Tile> tile;
    Point current_pos(x, y);
    switch(c) {
      case '#':
        tile.reset(new Wall(current_pos));
        break;
      case ' ':
        tile.reset(new Space(current_pos));
        break;
      case '@':
        tile.reset(new Space(current_pos));
        start = current_pos;
        break;
      case '\n':
        ++y;
        if (x > max_x) {
          max_x = x;
        }
        x = 0;
      default:
        return makeMapStatusBadTile;
    }
    ++x;
  }
  return makeMapStatusOk;
}
