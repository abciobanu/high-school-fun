#include "../include/game_states.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdexcept>
#include <thread>

#include <termios.h>

#include "../include/raw_mode.h"

void load_configuration(const std::string &fname, std::vector<std::vector<bool>> &board)
{
    std::ifstream ifs(fname);
    while (ifs)
    {
        unsigned i, j;
        ifs >> i >> j;
        board.at(i).at(j) = true; // board[i][j] = true; but with bound-checking
    }

    if (!ifs && !ifs.eof())
        throw std::runtime_error("The file does not exist or it is something wrong with the file!");
    else
        std::cout << "Initial configuration loaded!\n";
}

void clear()
{ // These ANSI escape codes clear the screen and move the cursor to upper-left
    std::cout << "\x1b[2J\x1b[H" << std::flush;
}

void display_board(std::vector<std::vector<bool>> &board)
{
    size_t board_size = board.size();

    for (size_t i = 0; i < (2 * (board_size + 1)); ++i)
        std::cout << '#'; // top border
    std::cout << '\n';

    for (std::vector<bool> &v : board)
    {
        std::cout << '#'; // left border
        for (bool cell : v)
            std::cout << ((cell) ? ("■") : (" ")) << ' ';
        std::cout << "#\n"; // right border
    }

    for (size_t i = 0; i < (2 * (board_size + 1)); ++i)
        std::cout << '#'; // bottom border
    std::cout << '\n';
}

void start_game(std::vector<std::vector<bool>> &board)
{
    clear();
    enable_raw_mode();

    size_t board_size = board.size();
    std::vector<std::vector<bool>> next_board(board_size, std::vector<bool>(board_size));

    bool repeat = true;
    while (repeat)
    {
        if (kbhit())
        {
            char ch = getchar();
            if (tolower(ch) == 'q')
                repeat = false;
        }

        auto start_time = std::chrono::high_resolution_clock::now();

        clear();
        display_board(board);

        for (size_t i = 0; i < board_size; ++i)
            for (size_t j = 0; j < board_size; ++j)
            {
                unsigned int neighbours = 0;

                // the neighbouring cell on the top left
                neighbours += board[(i - 1 + board_size) % board_size][(j - 1 + board_size) % board_size];

                // the neighbouring cell on the top
                neighbours += board[(i - 1 + board_size) % board_size][j % board_size];

                // the neighbouring cell on the top right
                neighbours += board[(i - 1 + board_size) % board_size][(j + 1) % board_size];

                // the neighbouring cell on the left
                neighbours += board[i % board_size][(j - 1 + board_size) % board_size];

                // the neighbouring cell on the right
                neighbours += board[i % board_size][(j + 1) % board_size];

                // the neighbouring cell on the bottom left
                neighbours += board[(i + 1) % board_size][(j - 1 + board_size) % board_size];

                // the neighbouring cell on the bottom
                neighbours += board[(i + 1) % board_size][j % board_size];

                // the neighbouring cell on the bottom right
                neighbours += board[(i + 1) % board_size][(j + 1) % board_size];

                if (neighbours < 2 || neighbours > 3)
                    next_board[i][j] = false;
                else if (board[i][j])
                    next_board[i][j] = true;
                else if (neighbours == 3)
                    next_board[i][j] = true;
            }

        board = next_board;

        auto end_time = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = end_time - start_time;
        std::this_thread::sleep_for(std::chrono::milliseconds(100) - duration); // for constant framerate
    }

    disable_raw_mode();
    tcflush(0, TCIFLUSH);
    clear();
}
