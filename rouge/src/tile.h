#ifndef TILE_H_
#define TILE_H_

#include <memory>

#include "point.h"

class Tile {
  protected:
    Point point;

    Tile(Point p): point(p) {}

  public:
    virtual ~Tile();
    virtual char display() = 0;
};

class Wall: public Tile {
  public:
    Wall(Point p): Tile(p) {}

    char display() {
      return '#';
    }
};

class Space: public Tile {
  public:
    Space(Point p): Tile(p) {}

    char display() {
      return ' ';
    }
};

#endif // TILE_H_
