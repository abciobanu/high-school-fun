#ifndef GAME_STATES_H
#define GAME_STATES_H

class Game_field;

void clear();
void pause_game();
void exit_game();
bool end_game();
void print_pregame(Game_field &);
void game_loop(Game_field &, bool &);

#endif // GAME_STATES
