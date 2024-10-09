from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox, \
    QHBoxLayout

from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver


class SudokuGUI(QMainWindow):
    def __init__(self, difficulty, back_to_menu_callback):
        super().__init__()
        self.difficulty = difficulty
        self.size = 4 if difficulty == "4x4" else 9  # Thêm kích thước lưới
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 400 if self.size == 4 else 500, 500 if self.size == 4 else 600)

        self.back_to_menu_callback = back_to_menu_callback

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.main_layout.addLayout(self.grid_layout)

        self.cells = []
        cell_size = 80 if self.size == 4 else 50  # Điều chỉnh kích thước ô dựa trên kích thước lưới
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFont(QFont("Arial", 18))
                cell.setMaxLength(1)
                cell.setFixedSize(cell_size, cell_size)  # Đảm bảo ô là hình vuông
                cell.setStyleSheet("background-color: white; border: 2px solid #000;")
                self.grid_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)

        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.check_button = QPushButton("Check")
        self.check_button.setFont(QFont("Arial", 14))
        self.check_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px; padding: 10px;")
        self.check_button.clicked.connect(self.check_solution)
        self.button_layout.addWidget(self.check_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.setFont(QFont("Arial", 14))
        self.solve_button.setStyleSheet("background-color: #FF6347; color: white; border-radius: 5px; padding: 10px;")
        self.solve_button.clicked.connect(self.solve_sudoku)
        self.button_layout.addWidget(self.solve_button)

        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setFont(QFont("Arial", 14))
        self.new_game_button.setStyleSheet(
            "background-color: #1E90FF; color: white; border-radius: 5px; padding: 10px;")
        self.new_game_button.clicked.connect(self.new_game)
        self.button_layout.addWidget(self.new_game_button)

        self.exit_button = QPushButton("Exit to Menu")
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.setStyleSheet("background-color: #808080; color: white; border-radius: 5px; padding: 10px;")
        self.exit_button.clicked.connect(self.exit_to_menu)
        self.button_layout.addWidget(self.exit_button)

        self.new_game()

    def new_game(self):
        sudoku_generator = SudokuGenerator(self.size)
        self.grid = sudoku_generator.generate_puzzle(self.difficulty)

        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != 0:
                    self.cells[i][j].setText(str(self.grid[i][j]))
                    self.cells[i][j].setReadOnly(True)
                    self.cells[i][j].setStyleSheet("background-color: lightgray;")
                else:
                    self.cells[i][j].setText("")
                    self.cells[i][j].setReadOnly(False)
                    self.cells[i][j].setStyleSheet("background-color: white;")

    def check_solution(self):
        # Lưu trữ trạng thái màu nền ban đầu
        original_styles = []
        for i in range(self.size):
            row_styles = []
            for j in range(self.size):
                row_styles.append(self.cells[i][j].styleSheet())
            original_styles.append(row_styles)

        # Kiểm tra giải pháp của người dùng
        user_solution = []
        is_complete = True
        incorrect_cells = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                try:
                    val = int(self.cells[i][j].text())
                except ValueError:
                    val = 0
                row.append(val)
                if val == 0:
                    is_complete = False
            user_solution.append(row)

        # Tạo một bản sao của lưới Sudoku để không làm thay đổi lưới ban đầu
        grid_copy = [row[:] for row in self.grid]

        # Tạo đối tượng SudokuSolver với lưới sao chép
        solver = SudokuSolver(grid_copy)
        if solver.solve():
            correct_solution = solver.grid
            incorrect_found = False
            for i in range(self.size):
                for j in range(self.size):
                    if user_solution[i][j] != correct_solution[i][j]:
                        self.cells[i][j].setStyleSheet("background-color: red; border: 2px solid #000;")
                        incorrect_cells.append((i, j))
                        incorrect_found = True

            if incorrect_found:
                QMessageBox.warning(self, "Oops!", "Some cells are incorrect. Please try again.")
                # Trả lại trạng thái màu nền ban đầu cho các ô sai
                for i, j in incorrect_cells:
                    self.cells[i][j].setStyleSheet(original_styles[i][j])
            elif not is_complete:
                QMessageBox.information(self, "Incomplete", "The puzzle is incomplete. Please fill in all the cells.")
            else:
                QMessageBox.information(self, "Congratulations!", "You solved the puzzle correctly!")
        else:
            QMessageBox.warning(self, "Error", "Could not solve the puzzle. Please check your input.")

    def solve_sudoku(self):
        solver = SudokuSolver(self.grid)
        self.solve_steps = solver.solve()
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.timer.start(10)

    def show_next_step(self):
        if self.step_index < len(self.solve_steps):
            row, col, num = self.solve_steps[self.step_index]
            if num == 0:
                self.cells[row][col].setText("")
                self.cells[row][col].setStyleSheet(
                    "background-color: white; border: 2px solid #000; border-radius: 5px;")
            else:
                self.cells[row][col].setText(str(num))
                self.cells[row][col].setStyleSheet(
                    "background-color: lightgreen; border: 2px solid #000; border-radius: 5px;")
            self.step_index += 1
        else:
            self.timer.stop()
            QMessageBox.information(self, "Solved", "The puzzle was solved successfully.")

    def exit_to_menu(self):
        self.close()
        self.back_to_menu_callback()
