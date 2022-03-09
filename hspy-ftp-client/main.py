from tkinter import Tk
import window


def main():
    root = Tk()
    main_window = window.MainWindow(root)

    main_window.master.mainloop()


if __name__ == '__main__':
    main()
