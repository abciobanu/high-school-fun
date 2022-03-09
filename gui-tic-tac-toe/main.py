from tkinter import Tk, messagebox

import windows


# Symbol selection window
root = Tk()
first_window = windows.First_window(root)

root.mainloop()

player_symbol = first_window.chosen_symbol
if player_symbol == ' ':
    exit()

computer_symbol = 'O' if player_symbol == 'X' else 'X'

game_field = [
    ' ', ' ', ' ',
    ' ', ' ', ' ',
    ' ', ' ', ' '
]

points = {
    computer_symbol: 1,
    player_symbol: -1,
    'tie': 0
}


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


def display_winner_window(result):
    if result == 'tie':
        messagebox.showinfo(title='Game over', message='It\'s a tie!')
    else:
        messagebox.showinfo(title='Game over', message=f'\'{result}\' wins!')

    exit()


def main():
    main = Tk()
    main_window = windows.Main_window(main)

    if player_symbol == 'O':
        game_field[0] = computer_symbol
        main_window.draw_symbol(computer_symbol, 0)

    def get_mouse_click(event):
        click_coords = (event.x, event.y)
        position = main_window.coords_to_grid(click_coords)

        if game_field[position] == ' ':
            game_field[position] = player_symbol
            main_window.draw_symbol(player_symbol, position)

            winner = check_winner()
            if winner is not None:
                display_winner_window(winner)
            else:
                best_position = find_move()
                game_field[best_position] = computer_symbol
                main_window.draw_symbol(computer_symbol, best_position)

                winner = check_winner()
                if winner is not None:
                    display_winner_window(winner)

    main_window.canvas.bind('<Button 1>', get_mouse_click)

    main.mainloop()


if __name__ == '__main__':
    main()
