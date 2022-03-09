#include "../include/point.h"

#include <stdexcept>

extern const unsigned int WIDTH, HEIGHT;

Point::Point(unsigned x, unsigned y)
{
    if (x < WIDTH && y < HEIGHT)
    {
        this->x = x;
        this->y = y;
    }
    else
        throw std::runtime_error("Invalid Point member initializers!");
}

bool operator==(Point a, Point b)
{
    return ((a.x == b.x) && (a.y == b.y));
}
