import tkinter as tk

from gui import MinesweeperGUI


def intermediate_example():
    """
    Start Minesweeper op Intermediate-niveau:
    16x16 met 40 mijnen.
    """

    root = tk.Tk()

    app = MinesweeperGUI(root)

    app.rows = 16
    app.columns = 16
    app.number_of_mines = 40

    app.create_game()

    root.mainloop()


if __name__ == "__main__":
    intermediate_example()