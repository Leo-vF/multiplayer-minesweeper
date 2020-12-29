from numpy.random import choice
from numpy import ravel


class Minesweeper:
    def __init__(self, start_col: int, start_row: int, n_rows: int = 20, n_cols: int = 30):
        self.field = [[Spot(col, row) for row in range(n_cols)]
                      for col in range(n_rows)]
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.n_spots = n_cols * n_rows
        self.start_pos = (start_col, start_row)

    def __str__(self) -> str:
        _str = "["
        for row in self.field:
            _str += ("[")
            for spot in row:
                _str += str(spot) + ", "
            _str = _str[:-2] + "], \n"
        _str = _str[:-3] + "]"
        return _str

    def place_mines(self):
        """Makes a consistent minesweeper field that you can't lose in, on the first try. 1 of 6 spots in the field are mines.
        """
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

    def test_solver(self):
        """Used to test wether or not a board is solvable purely by logic.
        The solver treats Minesweeper as a constraint satisfaction problem with depth first search to open all fields that have no mines as neighbors
        """
        moves = []
        spots_to_probe = []


class Spot:
    def __init__(self, col: int, row: int):
        self.row: int = row
        self.col: int = col
        self.n_mines: int = 0
        self.orig_n_mines: int = 0
        self.mine: bool = None
        self.constraints: list[tuple[int, int]] = None

    def __str__(self):
        str = f"({self.col}, {self.row})"
        return str

    def setMine(self):
        self.mine = True

    def setN_mines(self, n_mines: int):
        self.n_mines = n_mines
        self.orig_n_Mines = n_mines

    def get_col_row(self):
        return (self.col, self.row)


if __name__ == "__main__":
    ms = Minesweeper(1, 1, 5, 2)
    ms.place_mines()
    for row in ms.field:
        for spot in row:
            print(spot.mine)
