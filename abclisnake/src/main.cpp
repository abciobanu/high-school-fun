#include <iostream>

#include "../include/game_field.h"
#include "../include/raw_mode.h"
#include "../include/game_states.h"

extern const unsigned int HEIGHT = 15; // Height constant of the game field
extern const unsigned int WIDTH = 30;  // Width constant of the game field

int main()
try
{
    bool restart = false;
    do
    {
        Game_field g_field;
        print_pregame(g_field);
        game_loop(g_field, restart);
    } while (restart);

    return 0;
}
catch (std::exception &e)
{
    std::cerr << e.what() << '\n';
    return 1;
}
catch (...)
{
    std::cerr << "Unknown exception!\n";
    return 2;
}
