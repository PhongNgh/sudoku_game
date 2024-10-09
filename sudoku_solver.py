class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.box_size = int(self.size ** 0.5)
        self.solve_steps = []

    def is_valid(self, row, col, num):
        for x in range(self.size):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self):
        self.solve_steps = []
        self._solve()
        return self.solve_steps

    def _solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True

        row, col = empty
        for num in range(1, self.size + 1):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                self.solve_steps.append((row, col, num))
                if self._solve():
                    return True
                self.grid[row][col] = 0
                self.solve_steps.append((row, col, 0))

        return False

    def find_empty_location(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
