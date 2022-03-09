#ifndef GAME_STATES_H
#define GAME_STATES_H

#include <string>
#include <vector>

void load_configuration(const std::string &, std::vector<std::vector<bool>> &);
void start_game(std::vector<std::vector<bool>> &);

#endif // GAME_STATES_H
