#include "../include/game_field.h"

#include <iostream>
#include <cstdlib>
#include <ctime>

#include "../include/point.h"

extern const unsigned int WIDTH, HEIGHT;

Game_field::Game_field()
    : width(WIDTH), height(HEIGHT), score(0)
{   
    for (unsigned int i = 1; i <= height; ++i)
        Game_field::g_field.push_back(std::vector<char>(width, ' '));

    std::srand(time(NULL)); // sets random seed depending on the time
    
    // generates random snake x and y coordinates
    unsigned int snake_x = rand() % WIDTH;
    unsigned int snake_y = rand() % HEIGHT; 
    Game_field::snake.change_head_position(Point{snake_x, snake_y});

    generate_food();

    update_epos(); // updates game elements on the field
}

Game_field::Game_field(unsigned int w, unsigned int h, Elements::Snake s, Elements::Fruit f)
    : width(w), height(h), snake(s), fruit(f), score(0)
{
    for (unsigned int i = 1; i <= height; ++i)
        Game_field::g_field.push_back(std::vector<char>(width, ' '));

    update_epos(); // updates game elements on the field
}

void Game_field::update_field()
{   // updates the field with all new coordinates
    for (auto& row : g_field)
        for (char& ch : row)
            ch = ' ';
    
    update_epos();  // snake's and fruit's position update to the game field
}

void Game_field::update_epos()
{   // updates snake's and fruit's coordinates on the game field
    Point f_pos = fruit.get_position();
    g_field[f_pos.y][f_pos.x] = '@'; // '@' = fruit's symbol

    auto snake_elements = snake.get_body_elements();
    for (auto element : snake_elements)
        g_field[element.y][element.x] = 'X'; // 'X' = snake's body element symbol

    Point s_pos = snake.get_head_position();
    g_field[s_pos.y][s_pos.x] = 'O'; // 'O' = snake's head symbol
}

void move_snake(Game_field& g_f, bool& has_moved)
{   // moves the snake on the game field to one of the following directions:
    // 1 == UP, 2 == DOWN, 3 == LEFT, 4 == RIGHT
    // (The function returns false if the snake goes outbound.
    // Otherwise, the function returns true.)
    Direction snake_direction = g_f.snake.get_direction();
    Point snake_head_position = g_f.snake.get_head_position();

    switch (snake_direction)
    {
    case Direction::UP:
        // if the snake is right below the upper border, it can't go up anymore
        if (snake_head_position.y == 0) has_moved = false;
        else
        {   
            if (g_f.snake.get_length() == 1) g_f.snake.change_head_position(snake_direction); // moves only the head
            else g_f.snake.move(); // moves the whole snake
            has_moved = true;
        }
        break;
    
    case Direction::DOWN:
        // if the snake is right above the bottom border, it can't go down anymore
        if (snake_head_position.y == HEIGHT - 1) has_moved = false;
        else
        {
            if (g_f.snake.get_length() == 1) g_f.snake.change_head_position(snake_direction);
            else g_f.snake.move();
            has_moved = true;
        }
        break;
    
    case Direction::LEFT:
        // if the snake is right next to the left border, it can't go left anymore
        if (snake_head_position.x == 0) has_moved = false;
        else
        {
            if (g_f.snake.get_length() == 1) g_f.snake.change_head_position(snake_direction);
            else g_f.snake.move();
            has_moved = true;
        }
        break;
    
    case Direction::RIGHT:
        // if the snake is right next to the right border, it can't go right anymore
        if (snake_head_position.x == WIDTH - 1) has_moved = false;
        else
        {
            if (g_f.snake.get_length() == 1) g_f.snake.change_head_position(snake_direction);
            else g_f.snake.move();
            has_moved = true;
        }
        break;
    
    default:
        break;
    }

    g_f.update_field();
}

void Game_field::generate_food()
{   // generates new food (fruit)
    unsigned int fruit_x = rand() % WIDTH;
    unsigned int fruit_y = rand() % HEIGHT;
    Game_field::fruit.change_position(Point{fruit_x, fruit_y}); // set fruit's position to a random position

    update_field();
}

void Game_field::check_food()
{   // checks if the food has been "eaten" by the snake
    // if so, the score and snake's length are increased and a new fruit is generated
    if (snake.get_head_position() == fruit.get_position())
    {  
        increase_score();
        snake.increase_length();
        generate_food();
    }
}

void draw_field(const Game_field& gf)
{   // draws the border, the field and the score to the console
    std::cout << "Score: " << gf.score << '\n';
    
    for (unsigned int i = 0; i <= gf.get_width() + 1; ++i) std::cout << '#';
    std::cout << '\n';
    
    for (unsigned int i = 0; i < gf.get_height(); ++i)
    {
        std::cout << '#';
        for (unsigned int j = 0; j < gf.get_width(); ++j) std::cout << gf.g_field[i][j];
        std::cout << "#\n";
    }

    for (unsigned int i = 0; i <= gf.get_width() + 1; ++i) std::cout << '#';
    std::cout << '\n';
}
