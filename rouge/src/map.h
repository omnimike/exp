#ifndef MAP_H_
#define MAP_H_

#include <string>
#include <memory>
#include <vector>

#include "tile.h"

class Map {

  public:
    static std::unique_ptr<Map> default_map();
    void render();

  private:
    std::unique_ptr<std::vector<Tile>> tiles;
    Map(std::unique_ptr<std::vector<Tile>> tiles) : tiles(std::move(tiles)) {}
};

#endif // MAP_H_
