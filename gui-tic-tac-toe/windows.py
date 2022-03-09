from sys import platform
from tkinter import Tk, Label, Button, Canvas, BOTH, Misc


class First_window:
    def __init__(self, master):
        self.master = master

        if platform == "win32":
            master.iconbitmap('icon.ico')
        else:
            master.wm_iconbitmap(bitmap='@icon.xbm')

        master.title('Tic-tac-toe')
        master.geometry('256x128')
        master.resizable(0, 0)

        self.label = Label(master, text='Choose your symbol:')
        self.label.pack()

        self.x_button = Button(
            master, text='X', command=lambda: self.set_symbol('X'))
        self.x_button.pack()

        self.o_button = Button(
            master, text='O', command=lambda: self.set_symbol('O'))
        self.o_button.pack()

        self.chosen_symbol = ' '

    def set_symbol(self, symbol):
        self.chosen_symbol = symbol
        self.master.destroy()


class Main_window:
    def __init__(self, master, grid_thickness=2):
        self.master = master

        if platform == "win32":
            master.iconbitmap('icon.ico')
        else:
            master.wm_iconbitmap(bitmap='@icon.xbm')

        master.title('Tic-tac-toe')
        master.geometry('256x256')
        master.resizable(0, 0)

        self.canvas = Canvas()
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.update()

        self.draw_grid(grid_thickness)

    def draw_grid(self, thickness):
        self.canvas.create_line(0, self.canvas.winfo_height() / 3,
                                self.canvas.winfo_width(), self.canvas.winfo_height() / 3,
                                width=thickness)

        self.canvas.create_line(0, 2 * self.canvas.winfo_height() / 3,
                                self.canvas.winfo_width(), 2 * self.canvas.winfo_height() / 3,
                                width=thickness)

        self.canvas.create_line(self.canvas.winfo_width() / 3, 0,
                                self.canvas.winfo_width() / 3, self.canvas.winfo_height(),
                                width=thickness)

        self.canvas.create_line(2 * self.canvas.winfo_width() / 3, 0,
                                2 * self.canvas.winfo_width() / 3, self.canvas.winfo_height(),
                                width=thickness)

    def draw_symbol(self, symbol, position, offset=10, thickness=2):
        x_left = (position % 3) * (self.canvas.winfo_width() / 3) + offset
        y_up = int(position / 3) * (self.canvas.winfo_height() / 3) + offset
        x_right = (position % 3 + 1) * (self.canvas.winfo_width() / 3) - offset
        y_down = int(position / 3 + 1) * \
            (self.canvas.winfo_height() / 3) - offset

        if symbol == 'X':
            self.canvas.create_line(
                x_left, y_up, x_right, y_down, width=thickness)
            self.canvas.create_line(
                x_right, y_up, x_left, y_down, width=thickness)
        else:
            self.canvas.create_oval(
                x_left, y_up, x_right, y_down, width=thickness)

    def coords_to_grid(self, coordinates):
        x = int(coordinates[0])
        y = int(coordinates[1])
        if x < self.canvas.winfo_width() / 3:
            if y < self.canvas.winfo_height() / 3:
                return 0
            elif y < 2 * self.canvas.winfo_height() / 3:
                return 3
            elif y < self.canvas.winfo_height():
                return 6
        elif x < 2 * self.canvas.winfo_width() / 3:
            if y < self.canvas.winfo_height() / 3:
                return 1
            elif y < 2 * self.canvas.winfo_height() / 3:
                return 4
            elif y < self.canvas.winfo_height():
                return 7
        elif x < self.canvas.winfo_width():
            if y < self.canvas.winfo_height() / 3:
                return 2
            elif y < 2 * self.canvas.winfo_height() / 3:
                return 5
            elif y < self.canvas.winfo_height():
                return 8
