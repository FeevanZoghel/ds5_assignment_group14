import unittest

from board import (
    create_board,
    place_mines,
    count_neighbouring_mines,
    calculate_numbers,
    generate_board
)


class TestBoard(unittest.TestCase):
    """
    Tests voor de functies uit board.py.
    """

    def test_create_board_size(self):
        """
        Test of het bord het juiste aantal rijen en kolommen heeft.
        """

        board = create_board(9, 9)

        self.assertEqual(len(board), 9)

        for row in board:
            self.assertEqual(len(row), 9)


    def test_create_board_contains_zeros(self):
        """
        Test of een nieuw bord alleen nullen bevat.
        """

        board = create_board(5, 5)

        for row in board:
            for cell in row:
                self.assertEqual(cell, 0)


    def test_place_mines(self):
        """
        Test of het juiste aantal mijnen wordt geplaatst.
        """

        board = create_board(9, 9)

        board = place_mines(board, 10)

        mine_count = 0

        for row in board:
            for cell in row:

                if cell == -1:
                    mine_count += 1

        self.assertEqual(mine_count, 10)


    def test_no_duplicate_mines(self):
        """
        Test of er niet meerdere mijnen op hetzelfde vakje
        worden geplaatst.
        """

        board = create_board(9, 9)

        board = place_mines(board, 10)

        mine_count = sum(
            row.count(-1)
            for row in board
        )

        self.assertEqual(mine_count, 10)


    def test_count_neighbouring_mines(self):
        """
        Test of omliggende mijnen correct worden geteld.
        """

        board = [
            [-1, 0, 0],
            [0, 0, 0],
            [0, 0, -1]
        ]

        # Het middelste vakje heeft twee mijnen als buur
        result = count_neighbouring_mines(
            board,
            1,
            1
        )

        self.assertEqual(result, 2)


    def test_count_neighbouring_mines_corner(self):
        """
        Test het tellen van mijnen vanuit een hoek van het bord.
        """

        board = [
            [0, -1, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        result = count_neighbouring_mines(
            board,
            0,
            0
        )

        self.assertEqual(result, 1)


    def test_calculate_numbers(self):
        """
        Test of de juiste getallen op het bord worden gezet.
        """

        board = [
            [-1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        board = calculate_numbers(board)

        expected_board = [
            [-1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        self.assertEqual(
            board,
            expected_board
        )


    def test_generate_board_size(self):
        """
        Test of generate_board een bord met de juiste
        afmetingen maakt.
        """

        board = generate_board(9, 9, 10)

        self.assertEqual(len(board), 9)

        for row in board:
            self.assertEqual(len(row), 9)


    def test_generate_board_number_of_mines(self):
        """
        Test of generate_board het juiste aantal mijnen bevat.
        """

        board = generate_board(9, 9, 10)

        mine_count = 0

        for row in board:
            for cell in row:

                if cell == -1:
                    mine_count += 1

        self.assertEqual(
            mine_count,
            10
        )


    def test_generated_values(self):
        """
        Test of alle waarden op een gegenereerd bord geldig zijn.

        -1 betekent een mijn.
        0 t/m 8 is het aantal omliggende mijnen.
        """

        board = generate_board(9, 9, 10)

        for row in board:
            for cell in row:

                self.assertTrue(
                    -1 <= cell <= 8
                )


if __name__ == "__main__":
    unittest.main()