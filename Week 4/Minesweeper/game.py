from board import generate_board


class MinesweeperGame:
    """
    Regelt de spelregels van Minesweeper.

    Het bord zelf wordt gemaakt in board.py.
    """

    def __init__(self, rows: int, columns: int, number_of_mines: int):
        """
        Maakt een nieuw Minesweeper-spel.

        Parameters:
            rows: Het aantal rijen.
            columns: Het aantal kolommen.
            number_of_mines: Het aantal mijnen.
        """

        self.rows = rows
        self.columns = columns
        self.number_of_mines = number_of_mines

        self.board = generate_board(
            rows,
            columns,
            number_of_mines
        )

        # Houdt bij welke vakjes geopend zijn
        self.opened = []

        for row in range(rows):
            new_row = []

            for column in range(columns):
                new_row.append(False)

            self.opened.append(new_row)

        # Houdt bij waar de speler vlaggetjes heeft geplaatst
        self.flagged = []

        for row in range(rows):
            new_row = []

            for column in range(columns):
                new_row.append(False)

            self.flagged.append(new_row)

        self.score = 0
        self.game_over = False
        self.won = False


    def open_cell(self, row: int, column: int) -> str:
        """
        Opent een vakje.

        Returns:
            'mine' als het vakje een mijn bevat.
            'safe' als het vakje veilig is.
            'won' als alle veilige vakjes geopend zijn.
            'flagged' als het vakje gemarkeerd is.
        """

        # Niets meer doen als het spel afgelopen is
        if self.game_over:
            return "game_over"

        # Een vakje met een vlag mag niet geopend worden
        if self.flagged[row][column]:
            return "flagged"

        # Een geopend vakje niet opnieuw openen
        if self.opened[row][column]:
            return "already_open"

        # Speler heeft een mijn aangeklikt
        if self.board[row][column] == -1:
            self.opened[row][column] = True
            self.game_over = True
            return "mine"

        # Veilig vakje openen
        self.opened[row][column] = True
        self.score += 1

        # Als er geen mijnen omheen liggen,
        # moeten omliggende vakjes automatisch worden geopend
        if self.board[row][column] == 0:
            self.open_empty_cells(row, column)

        # Controleren of de speler gewonnen heeft
        if self.check_win():
            self.game_over = True
            self.won = True
            return "won"

        return "safe"


    def open_empty_cells(self, row: int, column: int):
        """
        Opent automatisch verbonden lege vakjes.

        Als een buurvakje ook waarde 0 heeft,
        worden de buren daarvan ook geopend.
        """

        for row_change in [-1, 0, 1]:
            for column_change in [-1, 0, 1]:

                if row_change == 0 and column_change == 0:
                    continue

                neighbour_row = row + row_change
                neighbour_column = column + column_change

                # Controleren of het vakje binnen het bord ligt
                if (
                    0 <= neighbour_row < self.rows
                    and 0 <= neighbour_column < self.columns
                ):

                    # Alleen nog gesloten en niet gemarkeerde vakjes openen
                    if (
                        not self.opened[neighbour_row][neighbour_column]
                        and not self.flagged[neighbour_row][neighbour_column]
                    ):

                        # Een mijn nooit automatisch openen
                        if self.board[neighbour_row][neighbour_column] != -1:

                            self.opened[neighbour_row][neighbour_column] = True
                            self.score += 1

                            # Als dit ook een leeg vakje is,
                            # verder zoeken vanaf dit vakje
                            if self.board[neighbour_row][neighbour_column] == 0:
                                self.open_empty_cells(
                                    neighbour_row,
                                    neighbour_column
                                )


    def toggle_flag(self, row: int, column: int):
        """
        Plaatst of verwijdert een vlag op een vakje.
        """

        if self.game_over:
            return

        # Op een geopend vakje kan geen vlag geplaatst worden
        if self.opened[row][column]:
            return

        if self.flagged[row][column]:
            self.flagged[row][column] = False
        else:
            self.flagged[row][column] = True


    def check_win(self) -> bool:
        """
        Controleert of alle vakjes zonder mijn geopend zijn.

        Returns:
            True als de speler gewonnen heeft.
            False als er nog veilige vakjes gesloten zijn.
        """

        for row in range(self.rows):
            for column in range(self.columns):

                if self.board[row][column] != -1:
                    if not self.opened[row][column]:
                        return False

        return True


    def reveal_mines(self):
        """
        Maakt alle mijnen zichtbaar.
        """

        for row in range(self.rows):
            for column in range(self.columns):

                if self.board[row][column] == -1:
                    self.opened[row][column] = True


    def give_up(self):
        """
        Beëindigt het spel en maakt alle mijnen zichtbaar.
        """

        self.reveal_mines()
        self.game_over = True

game = MinesweeperGame(9, 9, 10)

