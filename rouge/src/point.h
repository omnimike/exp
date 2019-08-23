#ifndef POINT_H_
#define POINT_H_

#include <stdint.h>
#include <stdlib.h>
#include <functional>

class Point {
  private:
    uint32_t _x;
    uint32_t _y;

  public:
    Point(): _x(0), _y(0) {}
    Point(uint32_t x, uint32_t y): _x(x), _y(y) {}

    uint32_t x() const {
      return _x;
    }

    uint32_t y() const {
      return _y;
    }

    Point add(const uint32_t delta_x, const uint32_t delta_y) const {
      return Point(_x + delta_x, _y + delta_y);
    }

    bool operator==(const Point &other) const { 
        return (_x == other._x && _y == other._y);
    }
};

#endif // POINT_H_
