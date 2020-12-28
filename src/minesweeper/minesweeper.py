from random import sample


class Minesweeper:
    def __init__(self, start_col: int, start_row: int, n_cols: int = 30, n_rows: int = 20):
        self.field = [[0 for i in range(n_rows)] for j in range(n_cols)]
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.n_spots = n_cols * n_rows
        self.start_pos = (start_col, start_row)

    def place_mines(self):
        """Makes a consistent minesweeper field that you can't lose in, on the first try. 1 of 6 spots in the field are mines.
        """
        mines_to_place = round(self.n_spots/6)
        mine_spots = sample(self.field, mines_to_place)

        # ensures that you can't lose on the first click
        while self.start_pos in mine_spots:
            mine_spots = sample(self.field, mines_to_place)

        for mine in mine_spots:
            col, row = mine
            self.field[col][row] = -1
            neighbors = [
                (col-1, row-1), (col, row-1), (col+1, row-1)
                (col-1, row),                 (col+1, row),
                (col-1, row+1), (col, row+1), (col+1, row+1)
            ]
            for n in neighbors:
                if self.field[n[0], n[1]] == -1:
                    continue
                if 0 <= n[0] < self.n_cols & 0 <= n[1] < self.n_rows:
                    self.field[n[0], n[1]] += 1
