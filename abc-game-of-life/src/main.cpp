#include <iostream>
#include <string>
#include <vector>
#include <cctype>
#include <cstring>

#include "../include/game_states.h"

int main(int argc, char *argv[])
try
{
    int board_size = 0;
    std::string filename;

    if (argc == 5) // 5 total required arguments
    {
        int i = 1; // argv[0] is the program's name, so start with argv[1]
        while (i < argc)
        {
            if (i < (argc - 1) && strcmp(argv[i], "--size") == 0)
            {
                ++i;
                board_size = std::stoi(argv[i]);
            }
            else if (i < (argc - 1) && strcmp(argv[i], "--file") == 0)
            {
                ++i;
                filename = argv[i];
            }
            else
                throw std::runtime_error("Invalid arguments!");

            ++i;
        }
    }
    else
        throw std::runtime_error("Usage: ./abc-game-of-life --size [SIZE] --file [FILE]");

    std::vector<std::vector<bool>> board(board_size, std::vector<bool>(board_size));
    load_configuration(filename, board);

    std::cout << "Welcome to Game of Life!\n";
    for (char choice = ' '; tolower(choice) != 'y';)
    {
        std::cout << "Would you want to start the cellular automaton? [y/n] ";
        std::cin >> choice;
        if (tolower(choice) == 'y')
            start_game(board);
        else if (tolower(choice) == 'n')
            break;
    }

    std::cout << "You exited the game!\n";
    return 0;
}
catch (const std::runtime_error &e)
{
    std::cerr << e.what() << '\n';
    return 1;
}
catch (...)
{
    std::cerr << "Unknown exception!\n";
    return 2;
}
