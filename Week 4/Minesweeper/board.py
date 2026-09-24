import random


def create_board(rows: int, columns: int) -> list:
    """
    Maakt een leeg Minesweeper-bord.

    Parameters:
        rows: Het aantal rijen.
        columns: Het aantal kolommen.

    Returns:
        Een leeg bord gevuld met nullen.
    """

    board = []

    for row in range(rows):
        new_row = []

        for column in range(columns):
            new_row.append(0)

        board.append(new_row)

    return board


def place_mines(board: list, number_of_mines: int) -> list:
    """
    Plaatst willekeurig mijnen op het bord.

    Een mijn wordt weergegeven met -1.

    Parameters:
        board: Het Minesweeper-bord.
        number_of_mines: Het aantal mijnen dat geplaatst moet worden.

    Returns:
        Het bord met de geplaatste mijnen.
    """

    rows = len(board)
    columns = len(board[0])

    mines_placed = 0

    while mines_placed < number_of_mines:

        row = random.randint(0, rows - 1)
        column = random.randint(0, columns - 1)

        # Alleen een mijn plaatsen als hier nog geen mijn ligt
        if board[row][column] != -1:
            board[row][column] = -1
            mines_placed += 1

    return board


def count_neighbouring_mines(board: list, row: int, column: int) -> int:
    """
    Telt hoeveel mijnen rondom één vakje liggen.

    Parameters:
        board: Het Minesweeper-bord.
        row: De rij van het vakje.
        column: De kolom van het vakje.

    Returns:
        Het aantal omliggende mijnen.
    """

    rows = len(board)
    columns = len(board[0])

    mine_count = 0

    # Controleer de 8 mogelijke buurvakjes
    for row_change in [-1, 0, 1]:
        for column_change in [-1, 0, 1]:

            # Het vakje zelf hoeven we niet te controleren
            if row_change == 0 and column_change == 0:
                continue

            neighbour_row = row + row_change
            neighbour_column = column + column_change

            # Controleren of het buurvakje binnen het bord ligt
            if (
                0 <= neighbour_row < rows
                and 0 <= neighbour_column < columns
            ):
                if board[neighbour_row][neighbour_column] == -1:
                    mine_count += 1

    return mine_count


def calculate_numbers(board: list) -> list:
    """
    Berekent voor ieder vakje hoeveel mijnen eromheen liggen.

    Parameters:
        board: Het bord met geplaatste mijnen.

    Returns:
        Het bord met de aantallen omliggende mijnen.
    """

    rows = len(board)
    columns = len(board[0])

    for row in range(rows):
        for column in range(columns):

            # Alleen berekenen wanneer het vakje geen mijn is
            if board[row][column] != -1:
                board[row][column] = count_neighbouring_mines(
                    board,
                    row,
                    column
                )

    return board


def generate_board(rows: int, columns: int, number_of_mines: int) -> list:
    """
    Maakt een compleet Minesweeper-bord.

    Parameters:
        rows: Het aantal rijen.
        columns: Het aantal kolommen.
        number_of_mines: Het aantal mijnen.

    Returns:
        Een compleet Minesweeper-bord.
    """

    board = create_board(rows, columns)

    board = place_mines(board, number_of_mines)

    board = calculate_numbers(board)

    return board
