from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class HelpScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Help")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Hướng Dẫn Chơi Sudoku")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Help Text
        help_text = QTextEdit()
        help_text.setText(
            "Sudoku là một trò chơi số dựa trên logic. Mục tiêu của trò chơi là điền vào một bảng 4x4 hoặc 9x9 các chữ số sao cho mỗi cột, mỗi hàng, và mỗi ô nhỏ chứa tất cả các chữ số chỉ một lần duy nhất.\n\n"
            "Đối với Sudoku 4x4:\n"
            "1. Điền các số từ 1 đến 4 vào bảng.\n"
            "2. Mỗi số phải xuất hiện đúng một lần trong mỗi hàng, cột, và ô vuông 2x2.\n\n"
            "Đối với Sudoku 9x9:\n"
            "1. Điền các số từ 1 đến 9 vào bảng.\n"
            "2. Mỗi số phải xuất hiện đúng một lần trong mỗi hàng, cột, và ô vuông 3x3.\n\n"
            "Sử dụng logic và suy luận để giải quyết câu đố. Chúc bạn may mắn!"
        )
        help_text.setReadOnly(True)
        layout.addWidget(help_text)

        # Close Button
        close_button = QPushButton("Đóng")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
