from tkinter import Tk

import windows


def main():
    root = Tk()
    main_window = windows.Main_window(root)

    main_window.get_stats()

    root.mainloop()


if __name__ == '__main__':
    main()
