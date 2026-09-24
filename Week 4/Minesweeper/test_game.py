import unittest

from game import MinesweeperGame


class TestGame(unittest.TestCase):
    """
    Tests voor de spelregels uit game.py.
    """

    def setUp(self):
        """
        Maakt voor iedere test een nieuw spel.

        Daarna vervangen we het willekeurige bord door een vast bord,
        zodat we precies weten waar de mijnen liggen.
        """

        self.game = MinesweeperGame(3, 3, 1)

        self.game.board = [
            [-1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]


    def test_start_score(self):
        """
        Test of de score aan het begin 0 is.
        """

        self.assertEqual(
            self.game.score,
            0
        )


    def test_game_not_over_at_start(self):
        """
        Test of het spel bij de start nog niet afgelopen is.
        """

        self.assertFalse(
            self.game.game_over
        )


    def test_open_safe_cell(self):
        """
        Test of een veilig vakje geopend wordt.
        """

        result = self.game.open_cell(0, 1)

        self.assertTrue(
            self.game.opened[0][1]
        )

        self.assertEqual(
            result,
            "safe"
        )


    def test_score_after_safe_cell(self):
        """
        Test of de score stijgt wanneer een veilig vakje
        wordt geopend.
        """

        self.game.open_cell(0, 1)

        self.assertEqual(
            self.game.score,
            1
        )


    def test_open_mine(self):
        """
        Test of het spel stopt wanneer een mijn wordt geopend.
        """

        result = self.game.open_cell(0, 0)

        self.assertEqual(
            result,
            "mine"
        )

        self.assertTrue(
            self.game.game_over
        )


    def test_mine_does_not_increase_score(self):
        """
        Test of het openen van een mijn geen punt oplevert.
        """

        self.game.open_cell(0, 0)

        self.assertEqual(
            self.game.score,
            0
        )


    def test_place_flag(self):
        """
        Test of een vlag geplaatst kan worden.
        """

        self.game.toggle_flag(0, 0)

        self.assertTrue(
            self.game.flagged[0][0]
        )


    def test_remove_flag(self):
        """
        Test of een vlag weer verwijderd kan worden.
        """

        self.game.toggle_flag(0, 0)
        self.game.toggle_flag(0, 0)

        self.assertFalse(
            self.game.flagged[0][0]
        )


    def test_flagged_cell_cannot_be_opened(self):
        """
        Test of een vakje met een vlag niet geopend kan worden.
        """

        self.game.toggle_flag(0, 1)

        result = self.game.open_cell(0, 1)

        self.assertEqual(
            result,
            "flagged"
        )

        self.assertFalse(
            self.game.opened[0][1]
        )


    def test_opened_cell_cannot_be_flagged(self):
        """
        Test of een geopend vakje niet meer gemarkeerd
        kan worden met een vlag.
        """

        self.game.open_cell(0, 1)

        self.game.toggle_flag(0, 1)

        self.assertFalse(
            self.game.flagged[0][1]
        )


    def test_open_same_cell_twice(self):
        """
        Test of hetzelfde vakje niet twee keer punten geeft.
        """

        self.game.open_cell(0, 1)

        result = self.game.open_cell(0, 1)

        self.assertEqual(
            result,
            "already_open"
        )

        self.assertEqual(
            self.game.score,
            1
        )


    def test_open_empty_cells(self):
        """
        Test of verbonden lege vakjes automatisch
        worden geopend.
        """

        self.game.open_cell(2, 2)

        self.assertTrue(
            self.game.opened[2][2]
        )

        self.assertTrue(
            self.game.opened[2][1]
        )

        self.assertTrue(
            self.game.opened[1][2]
        )


    def test_reveal_mines(self):
        """
        Test of reveal_mines alle mijnen zichtbaar maakt.
        """

        self.game.reveal_mines()

        self.assertTrue(
            self.game.opened[0][0]
        )


    def test_give_up(self):
        """
        Test of Give up het spel beëindigt
        en de mijnen zichtbaar maakt.
        """

        self.game.give_up()

        self.assertTrue(
            self.game.game_over
        )

        self.assertTrue(
            self.game.opened[0][0]
        )


    def test_win(self):
        """
        Test of de speler wint wanneer alle veilige
        vakjes geopend zijn.
        """

        # Voor deze test gebruiken we een klein bord
        game = MinesweeperGame(2, 2, 1)

        game.board = [
            [-1, 1],
            [1, 1]
        ]

        game.open_cell(0, 1)
        game.open_cell(1, 0)

        result = game.open_cell(1, 1)

        self.assertEqual(
            result,
            "won"
        )

        self.assertTrue(
            game.won
        )

        self.assertTrue(
            game.game_over
        )


    def test_no_moves_after_game_over(self):
        """
        Test of na game over geen nieuwe vakjes
        geopend kunnen worden.
        """

        # Eerst de mijn openen
        self.game.open_cell(0, 0)

        # Daarna proberen een veilig vakje te openen
        result = self.game.open_cell(0, 1)

        self.assertEqual(
            result,
            "game_over"
        )

        self.assertFalse(
            self.game.opened[0][1]
        )


if __name__ == "__main__":
    unittest.main()