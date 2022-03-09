#ifndef GAME_ELEMENTS_H
#define GAME_ELEMENTS_H

#include <vector>

#include "../include/point.h"

enum class Direction
{
    UP = 1,
    DOWN,
    LEFT,
    RIGHT
};

namespace Elements
{
    class Snake
    {
    public:
        Snake(Point p = Point{0, 0}, Direction d = Direction::UP) : head_position(p), direction(d) {}
        void change_head_position(Direction);
        void change_head_position(Point);
        const Point &get_head_position() const { return head_position; }
        void change_direction(Direction dir) { direction = dir; }
        const Direction &get_direction() const { return direction; }
        const std::vector<Point> &get_body_elements() const { return body_elements; }
        void move();
        bool check_body_collision();
        void increase_length();
        unsigned int get_length() { return body_elements.size() + 1; } // number of the body elements + its head
    private:
        Point head_position;
        std::vector<Point> body_elements;
        Direction direction;
    };

    struct Fruit
    {
    public:
        Fruit() : position(Point{0, 0}) {}
        Fruit(Point p) : position(p) {}
        void change_position(Point p) { position = p; }
        const Point &get_position() const { return position; }

    private:
        Point position;
    };
}

#endif // GAME_ELEMENTS_H
