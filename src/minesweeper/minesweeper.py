from numpy.random import choice
from numpy import ravel

from .spot import Spot


class Minesweeper:
    def __init__(self, n_cols: int, n_rows: int):
        self.field = [[Spot(col, row) for row in range(n_cols)]
                      for col in range(n_rows)]
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.n_spots = n_cols * n_rows

    def __str__(self) -> str:
        _str = "["
        for row in self.field:
            _str += ("[")
            for spot in row:
                _str += str(spot) + ", "
            _str = _str[:-2] + "], \n"
        _str = _str[:-3] + "]"
        return _str


    def place_mines(self, start_col: int, start_row: int):
        """Makes a consistent minesweeper field that you can't lose in, on the first try. 1 of 6 spots in the field are mines.
        """

        self.start_pos = self.field[start_col][start_row]

        mines_to_place = round(self.n_spots/6)
        mine_spots = choice(ravel(self.field), mines_to_place, replace=False)

        # ensures that you can't lose on the first click
        while self.start_pos in mine_spots:
            mine_spots = choice(ravel(self.field),
                                mines_to_place, replace=False)

        for mine in mine_spots:
            col, row = mine.get_col_row()
            self.field[col][row].mine = True
            neighbors = [
                (col-1, row-1), (col, row-1), (col+1, row-1),
                (col-1, row),                 (col+1, row),
                (col-1, row+1), (col, row+1), (col+1, row+1)
            ]
            for n in neighbors:
                if 0 <= n[0] < self.n_rows and 0 <= n[1] < self.n_cols:
                    if self.field[n[0]][n[1]].mine == True:
                        continue

                    self.field[n[0]][n[1]].n_mines += 1
                    self.field[n[0]][n[1]].orig_n_mines += 1

        # ensures that the field is solvable after the first click
        # meaning that the first field has to have 0 neighboring mines
        if self.start_pos.orig_n_mines != 0 or self.start_pos.mine == True:
            self.reset_field()
            self.place_mines()

    def reset_field(self):
        """Resets every Spot's number of mines and whether or not it is a mine
        """
        for row in self.field:
            for spot in row:
                spot.n_mines = 0
                spot.orig_n_mines = 0
                spot.mine = None

    def test_solver(self):
        """Used to test wether or not a board is solvable purely by logic.
        The solver treats Minesweeper as a constraint satisfaction problem with depth first search to open all fields that have no mines as neighbors
        """
        moves = []
        spots_to_probe = []


if __name__ == "__main__":
    ms = Minesweeper(2, 5, 1, 1)
    ms.place_mines()
    # for row in ms.field:
    #     for spot in row:
    #         print(spot.mine)
