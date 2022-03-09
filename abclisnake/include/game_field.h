#ifndef GAME_FIELD_H
#define GAME_FIELD_H

#include <vector>

#include "game_elements.h"

class Game_field
{
public:
    Game_field();
    Game_field(unsigned int w, unsigned int h, Elements::Snake s, Elements::Fruit f);
    unsigned int get_width() const { return width; }
    unsigned int get_height() const { return height; }
    void update_field();
    void change_sdir(Direction dir) { snake.change_direction(dir); }
    void check_food();
    bool is_body_colliding() { return snake.check_body_collision(); }
    void increase_score() { score++; }
    friend void move_snake(Game_field &, bool &);
    friend void draw_field(const Game_field &);

private:
    unsigned int width, height;
    Elements::Snake snake;
    Elements::Fruit fruit;
    unsigned int score;
    std::vector<std::vector<char>> g_field;
    void update_epos();
    void generate_food();
};

#endif // GAME_FIELD_H
