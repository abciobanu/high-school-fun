game_field = [
    ' ', ' ', ' ',
    ' ', ' ', ' ',
    ' ', ' ', ' '
]


def print_grid():
    print('-----')
    print(game_field[0] + '|' + game_field[1] + '|' + game_field[2])
    print('-+-+-')
    print(game_field[3] + '|' + game_field[4] + '|' + game_field[5])
    print('-+-+-')
    print(game_field[6] + '|' + game_field[7] + '|' + game_field[8])
    print('-----')
    print('=====')


def print_grid_instructions():
    print('-----')
    print('7|8|9')
    print('-+-+-')
    print('4|5|6')
    print('-+-+-')
    print('1|2|3')
    print('-----')
    print('=====')


def check_winner():
    for i in [0, 1, 2, 3, 6]:
        # Vertical
        if i in [0, 1, 2]:
            if game_field[i] == game_field[i + 3] == game_field[i + 6] and game_field[i] != ' ':
                return game_field[i]
        # Orizontal
        if i in [0, 3, 6]:
            if game_field[i] == game_field[i + 1] == game_field[i + 2] and game_field[i] != ' ':
                return game_field[i]

    # Diagonal
    if game_field[0] == game_field[4] == game_field[8] and game_field[0] != ' ':
        return game_field[0]
    if game_field[2] == game_field[4] == game_field[6] and game_field[2] != ' ':
        return game_field[2]

    # Check if the game is not finished yet
    for i in range(0, 9):
        if game_field[i] == ' ':
            return None

    return 'tie'


symbols = ['X', '0']

symbol_choice = int(input('Choose your symbol (0 for \'X\' or 1 for \'0\'): '))
player_symbol = symbols[symbol_choice]
computer_symbol = symbols[(symbol_choice + 1) % 2]

points = {
    computer_symbol: 1,
    player_symbol: -1,
    'tie': 0
}


def minimax(alpha, beta, is_maximizing):
    winner = check_winner()
    if winner is not None:
        return points[winner]

    if is_maximizing == True:
        best_score = -2

        for i in range(0, 9):
            if game_field[i] == ' ':
                game_field[i] = computer_symbol
                score = minimax(alpha, beta, False)
                game_field[i] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = 2

        for i in range(0, 9):
            if game_field[i] == ' ':
                game_field[i] = player_symbol
                score = minimax(alpha, beta, True)
                game_field[i] = ' '
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break

        return best_score


def find_move():
    best_score = -2
    best_move = -1

    for i in range(0, 9):
        if game_field[i] == ' ':
            game_field[i] = computer_symbol
            score = minimax(-2, 2, False)
            game_field[i] = ' '

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


input_to_index = {
    7: 0, 8: 1, 9: 2,
    4: 3, 5: 4, 6: 5,
    1: 6, 2: 7, 3: 8
}


def main():
    print_grid_instructions()

    turn = 'X'
    game_ended = False
    while game_ended == False:
        if turn == player_symbol:
            choice = 0
            while True:
                try:
                    choice = int(input('Your turn (1-9): '))
                    if game_field[input_to_index[choice]] != ' ':
                        raise Exception(
                            'The chosen position is already marked!')
                    break
                except ValueError:
                    print('Your input has to be a number between 1 and 9!')
                except Exception as e:
                    print(e)

            game_field[input_to_index[choice]] = player_symbol
            turn = computer_symbol

        else:
            best_position = find_move()
            game_field[best_position] = computer_symbol

            turn = player_symbol

        print_grid()

        winner = check_winner()
        if winner is not None:
            if winner == 'tie':
                print('Tie!')
            else:
                print(f'{winner} wins!')

            game_ended = True


if __name__ == '__main__':
    main()
