#include "../include/game_states.h"

#include <iostream>
#include <string>
#include <thread>

#include <termios.h>

#include "../include/raw_mode.h"
#include "../include/game_field.h"

void clear()
{ // These ANSI escape codes clear the screen and move the cursor to upper-left
    std::cout << "\x1b[2J\x1b[H" << std::flush;
}

void pause_game()
{ // pauses the game by waiting for the user to press 'p' again
    clear();
    std::cout << "Game is paused. Press [P] again to unpause the game.\n";

    char ch;
    while (true)
    {
        ch = getchar();
        if (ch == 'p')
            return;
    }
}

void exit_game()
{ // makes sure raw mode is disabled, clears stdin and then exits the game
    disable_raw_mode();
    tcflush(0, TCIFLUSH); // clears stdin to prevent characters appearing on prompt

    std::cout << "You exited the game!\n";
    clear();
    std::exit(1);
}

void ask_for_restart(bool &choice)
{ // asks the player if he wants to play again, and checks the input
    std::string answer;
    while (true)
    {
        std::cout << "You lost. Do you want to restart the game? [Y/n] ";
        std::getline(std::cin, answer);

        if (answer.length() == 0 || (answer.length() == 1 && std::tolower(answer[0]) == 'y'))
        { // if the player pressed [ENTER] or typed either 'y' or 'Y', he wants to play again
            choice = true;
            return;
        }
        else if (answer.length() == 1 && std::tolower(answer[0]) == 'n')
        { // if the player typed 'n' or 'N', he wants to exit the game
            choice = false;
            return;
        }
    }
}

void check_pregame_input(Game_field &g_f)
{ // waits for the player to choose the starting direction of the snake
    enable_raw_mode();
    while (true)
    {
        if (kbhit())
        {
            char ch = tolower(getchar());
            switch (ch)
            {
            case 'w':
                g_f.change_sdir(Direction::UP);
                return;

            case 's':
                g_f.change_sdir(Direction::DOWN);
                return;

            case 'a':
                g_f.change_sdir(Direction::LEFT);
                return;

            case 'd':
                g_f.change_sdir(Direction::RIGHT);
                return;

            case 'q':
                exit_game();
                return;

            default:
                break;
            }
        }
    }
    disable_raw_mode();
    tcflush(0, TCIFLUSH);
}

void print_pregame(Game_field &g_f)
{
    draw_field(g_f);
    std::cout << "Press any movement control key (W/A/S/D) to start the game!\n";
    check_pregame_input(g_f);
}

void check_ingame_input(Game_field &g_f)
{ // gets in-game input for the snake's direction and changes it
    enable_raw_mode();

    if (kbhit())
    {
        char ch = tolower(getchar());
        switch (ch)
        {
        case 'w':
            g_f.change_sdir(Direction::UP);
            return;

        case 's':
            g_f.change_sdir(Direction::DOWN);
            return;

        case 'a':
            g_f.change_sdir(Direction::LEFT);
            return;

        case 'd':
            g_f.change_sdir(Direction::RIGHT);
            return;

        case 'p':
            pause_game();
            return;

        case 'q':
            exit_game();
            return;

        default:
            break;
        }
    }

    disable_raw_mode();
}

void game_loop(Game_field &g_f, bool &restart)
{
    while (true)
    {
        auto start_time = std::chrono::high_resolution_clock::now();

        clear(); // clears the console

        check_ingame_input(g_f);

        bool snake_moved;
        move_snake(g_f, snake_moved);
        if (snake_moved == false || g_f.is_body_colliding() == true)
        {
            bool choice;
            ask_for_restart(choice);
            if (choice == true)
            { // player wants to play again
                restart = true;
                clear();
                return;
            }
            else
                exit_game();
        }

        g_f.check_food(); // checks if the food has been eaten

        draw_field(g_f);

        auto end_time = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = end_time - start_time;
        std::this_thread::sleep_for(std::chrono::milliseconds(200) - duration); // for constant framerate
    }
}
