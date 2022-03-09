#ifndef POINT_H
#define POINT_H

struct Point
{
    Point(unsigned int x = 0, unsigned int y = 0);
    unsigned int x, y;
};

bool operator==(Point, Point);

#endif // POINT_H
