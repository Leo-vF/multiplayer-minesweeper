class Spot:
    def __init__(self, col: int, row: int):
        self.row: int = row
        self.col: int = col
        self.n_mines: int = 0
        self.orig_n_mines: int = 0
        self.mine: bool = None
        self.constraints: list[tuple[int, int]] = None

    def __str__(self):
        str = f"({self.orig_n_mines}, {self.mine})"  # {self.col}, {self.row},
        return str

    def setMine(self):
        self.mine = True

    def setN_mines(self, n_mines: int):
        """Sets the Spot attributes n_mines and orig_n_mines to the parameter n_mines.

        Args:
            n_mines (int): The number of mines in neighobring spots
        """
        self.n_mines = n_mines
        self.orig_n_mines = n_mines

    def get_col_row(self) -> tuple:
        """Returns column and row of the spot

        Returns:
            tuple: Tuple with column and row
        """
        return (self.col, self.row)
