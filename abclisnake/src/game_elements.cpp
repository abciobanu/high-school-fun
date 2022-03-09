#include "../include/game_elements.h"

#include "../include/point.h"

extern const unsigned int WIDTH, HEIGHT;

namespace Elements
{
    void Snake::change_head_position(Direction d)
    { // moves the head to the given direction
        switch (d)
        {
        case Direction::UP:
            head_position = Point{head_position.x, head_position.y - 1};
            break;

        case Direction::DOWN:
            head_position = Point{head_position.x, head_position.y + 1};
            break;

        case Direction::LEFT:
            head_position = Point{head_position.x - 1, head_position.y};
            break;

        case Direction::RIGHT:
            head_position = Point{head_position.x + 1, head_position.y};
            break;

        default:
            break;
        }
    }

    void Snake::change_head_position(Point p)
    { // changes head's position to the given position
        if (p.x < HEIGHT && p.y < WIDTH)
            head_position = p;
    }

    void Snake::move()
    { // moves the snake to the set direction
        Point old_head_position = head_position;
        change_head_position(direction);

        for (unsigned int i = body_elements.size() - 1; i > 0; --i)
            body_elements[i] = body_elements[i - 1];
        // every element follows the successor
        body_elements[0] = old_head_position;
    }

    bool Snake::check_body_collision()
    { // checks if there's any head <-> body element collision
        for (auto element : body_elements)
            if (element == head_position)
                return true;

        return false;
    }

    void Snake::increase_length()
    { // increases snake's length by adding one more body element
        body_elements.push_back(get_head_position());
    }
}
