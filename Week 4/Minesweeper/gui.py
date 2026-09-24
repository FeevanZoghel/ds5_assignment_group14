import tkinter as tk
from tkinter import messagebox
import time

from game import MinesweeperGame


class MinesweeperGUI:
    """
    Grafische gebruikersinterface voor Minesweeper.

    De spelregels worden geregeld door MinesweeperGame in game.py.
    """

    def __init__(self, root: tk.Tk):
        """
        Maakt het Minesweeper-venster.
        """

        self.root = root
        self.root.title("Minesweeper")

        # Standaard moeilijkheid
        self.rows = 9
        self.columns = 9
        self.number_of_mines = 10

        self.game = None
        self.buttons = []

        self.start_time = 0
        self.timer_running = False

        self.create_top_menu()
        self.create_game()


    def create_top_menu(self):
        """
        Maakt het bovenste gedeelte met score, timer,
        instellingen en de Give up-knop.
        """

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.score_label = tk.Label(
            self.top_frame,
            text="Score: 0",
            font=("Arial", 12)
        )
        self.score_label.grid(row=0, column=0, padx=10)

        self.timer_label = tk.Label(
            self.top_frame,
            text="Time: 0 s",
            font=("Arial", 12)
        )
        self.timer_label.grid(row=0, column=1, padx=10)

        settings_button = tk.Button(
            self.top_frame,
            text="Settings",
            command=self.open_settings
        )
        settings_button.grid(row=0, column=2, padx=10)

        give_up_button = tk.Button(
            self.top_frame,
            text="Give up",
            command=self.give_up
        )
        give_up_button.grid(row=0, column=3, padx=10)


    def create_game(self):
        """
        Start een nieuw spel.
        """

        self.game = MinesweeperGame(
            self.rows,
            self.columns,
            self.number_of_mines
        )

        self.start_time = time.time()
        self.timer_running = True

        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="Time: 0 s")

        # Oud speelveld verwijderen
        if hasattr(self, "board_frame"):
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)

        self.buttons = []

        for row in range(self.rows):

            button_row = []

            for column in range(self.columns):

                button = tk.Button(
                    self.board_frame,
                    text="",
                    width=3,
                    height=1
                )

                button.grid(
                    row=row,
                    column=column
                )

                # Linkermuisknop
                button.config(
                    command=lambda r=row, c=column:
                    self.left_click(r, c)
                )

                # Rechtermuisknop
                button.bind(
                    "<Button-3>",
                    lambda event, r=row, c=column:
                    self.right_click(event, r, c)
                )

                button_row.append(button)

            self.buttons.append(button_row)

        self.update_timer()


    def left_click(self, row: int, column: int):
        """
        Wordt uitgevoerd wanneer de speler met links
        op een vakje klikt.
        """

        result = self.game.open_cell(row, column)

        self.update_board()

        if result == "mine":

            self.game.reveal_mines()
            self.update_board()

            self.end_game("You hit a mine!")

        elif result == "won":

            self.update_board()

            self.end_game("You won!")


    def right_click(self, event, row: int, column: int):
        """
        Plaatst of verwijdert een vlag met de rechtermuisknop.
        """

        self.game.toggle_flag(row, column)

        self.update_board()


    def update_board(self):
        """
        Werkt alle knoppen op het speelveld bij.
        """

        for row in range(self.rows):
            for column in range(self.columns):

                button = self.buttons[row][column]

                # Geopend vakje
                if self.game.opened[row][column]:

                    value = self.game.board[row][column]

                    if value == -1:
                        button.config(
                            text="💣",
                            state="disabled"
                        )

                    elif value == 0:
                        button.config(
                            text="",
                            state="disabled",
                            relief="sunken"
                        )

                    else:
                        button.config(
                            text=str(value),
                            state="disabled",
                            relief="sunken"
                        )

                # Vlag
                elif self.game.flagged[row][column]:

                    button.config(
                        text="🚩"
                    )

                # Nog gesloten vakje
                else:

                    button.config(
                        text="",
                        state="normal",
                        relief="raised"
                    )

        self.score_label.config(
            text=f"Score: {self.game.score}"
        )


    def update_timer(self):
        """
        Werkt iedere seconde de timer bij.
        """

        if self.timer_running:

            elapsed_time = int(
                time.time() - self.start_time
            )

            self.timer_label.config(
                text=f"Time: {elapsed_time} s"
            )

            self.root.after(
                1000,
                self.update_timer
            )


    def give_up(self):
        """
        Beëindigt het spel en toont alle mijnen.
        """

        if self.game.game_over:
            return

        self.game.give_up()

        self.update_board()

        self.end_game("You gave up!")


    def end_game(self, message: str):
        """
        Toont het eindscherm met score en tijd.
        """

        self.timer_running = False

        elapsed_time = int(
            time.time() - self.start_time
        )

        end_window = tk.Toplevel(self.root)
        end_window.title("Game over")

        tk.Label(
            end_window,
            text=message,
            font=("Arial", 16)
        ).pack(padx=30, pady=10)

        tk.Label(
            end_window,
            text=f"Score: {self.game.score}"
        ).pack(pady=5)

        tk.Label(
            end_window,
            text=f"Time: {elapsed_time} seconds"
        ).pack(pady=5)

        play_again_button = tk.Button(
            end_window,
            text="Play again",
            command=lambda:
            self.play_again(end_window)
        )

        play_again_button.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        exit_button = tk.Button(
            end_window,
            text="Exit",
            command=self.root.destroy
        )

        exit_button.pack(
            padx=20,
            pady=5,
            fill="x"
        )


    def play_again(self, window):
        """
        Sluit het eindscherm en start een nieuw spel.
        """

        window.destroy()

        self.create_game()


    def open_settings(self):
        """
        Opent een venster waarin de moeilijkheid
        gekozen kan worden.
        """

        settings_window = tk.Toplevel(self.root)

        settings_window.title("Settings")

        tk.Label(
            settings_window,
            text="Choose difficulty:",
            font=("Arial", 12)
        ).pack(padx=20, pady=10)

        beginner_button = tk.Button(
            settings_window,
            text="Beginner - 9x9 - 10 mines",
            command=lambda:
            self.change_difficulty(
                9,
                9,
                10,
                settings_window
            )
        )

        beginner_button.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        intermediate_button = tk.Button(
            settings_window,
            text="Intermediate - 16x16 - 40 mines",
            command=lambda:
            self.change_difficulty(
                16,
                16,
                40,
                settings_window
            )
        )

        intermediate_button.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        expert_button = tk.Button(
            settings_window,
            text="Expert - 30x16 - 99 mines",
            command=lambda:
            self.change_difficulty(
                16,
                30,
                99,
                settings_window
            )
        )

        expert_button.pack(
            padx=20,
            pady=5,
            fill="x"
        )


    def change_difficulty(
        self,
        rows: int,
        columns: int,
        mines: int,
        window
    ):
        """
        Verandert de moeilijkheid en start een nieuw spel.
        """

        self.rows = rows
        self.columns = columns
        self.number_of_mines = mines

        window.destroy()

        self.timer_running = False

        self.create_game()


def main():
    """
    Start de Minesweeper-applicatie.
    """

    root = tk.Tk()

    MinesweeperGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()