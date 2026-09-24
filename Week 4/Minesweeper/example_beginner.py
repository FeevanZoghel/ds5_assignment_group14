from game import MinesweeperGame


def beginner_example():
    """
    Voorbeeld van een Minesweeper-spel op Beginner-niveau.

    Beginner:
        - 9 rijen
        - 9 kolommen
        - 10 mijnen
    """

    game = MinesweeperGame(
        rows=9,
        columns=9,
        number_of_mines=10
    )

    print("Beginner Minesweeper")
    print("--------------------")
    print("Grid: 9 x 9")
    print("Mines: 10")
    print()

    # Laat het gegenereerde bord zien
    print("Generated board:")

    for row in game.board:
        print(row)

    print()

    # Voorbeeld van het openen van een vakje
    result = game.open_cell(0, 0)

    print("Cell (0, 0) opened.")
    print("Result:", result)
    print("Score:", game.score)

    print()

    # Voorbeeld van het plaatsen van een vlag
    if not game.opened[0][1]:
        game.toggle_flag(0, 1)

        print("Flag placed on cell (0, 1).")
        print("Flagged:", game.flagged[0][1])


if __name__ == "__main__":
    beginner_example()