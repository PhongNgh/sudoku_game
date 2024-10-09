import random
class SudokuGenerator:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.box_size = int(size ** 0.5)  # Sử dụng cho cả lưới 4x4 và 9x9
    def fill_grid(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_size)

    def fill_diagonal(self):
        for i in range(0, self.size, self.box_size):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        num_list = list(range(1, self.size + 1))
        random.shuffle(num_list)
        for i in range(self.box_size):
            for j in range(self.box_size):
                self.grid[row + i][col + j] = num_list.pop()

    def check_if_safe(self, i, j, num):
        return (self.unused_in_row(i, num) and
                self.unused_in_col(j, num) and
                self.unused_in_box(i - i % self.box_size, j - j % self.box_size, num))

    def unused_in_row(self, i, num):
        for j in range(self.size):
            if self.grid[i][j] == num:
                return False
        return True

    def unused_in_col(self, j, num):
        for i in range(self.size):
            if self.grid[i][j] == num:
                return False
        return True

    def unused_in_box(self, row_start, col_start, num):
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.grid[row_start + i][col_start + j] == num:
                    return False
        return True

    def fill_remaining(self, i, j):
        if j >= self.size and i < self.size - 1:
            i += 1
            j = 0
        if i >= self.size and j >= self.size:
            return True

        if i < self.box_size:
            if j < self.box_size:
                j = self.box_size
        elif i < self.size - self.box_size:
            if j == (i // self.box_size) * self.box_size:
                j += self.box_size
        else:
            if j == self.size - self.box_size:
                i += 1
                j = 0
                if i >= self.size:
                    return True

        for num in random.sample(range(1, self.size + 1), self.size):
            if self.check_if_safe(i, j, num):
                self.grid[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.grid[i][j] = 0

        return False

    def remove_digits(self, difficulty):
        cells_to_remove = self.size ** 2 // 2  # Xoá 1/2 số ô
        while cells_to_remove > 0:
            i = random.randint(0, self.size - 1)
            j = random.randint(0, self.size - 1)
            if self.grid[i][j] != 0:
                self.grid[i][j] = 0
                cells_to_remove -= 1

    def generate_puzzle(self, difficulty):
        self.__init__(4 if difficulty == "4x4" else 9)
        self.fill_grid()
        self.remove_digits(difficulty)
        return self.grid

