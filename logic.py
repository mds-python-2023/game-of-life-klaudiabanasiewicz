
import random

class GameOfLife:
    def __init__(self, width=50, height=50, randomize=True, file_path=None):
        self.width = width
        self.height = height
        if file_path:
            try:
                self.board = self.load_board_from_file(file_path)
                self.height = len(self.board)
                self.width = max(len(row) for row in self.board)
                self._normalize_board_dimensions()
            except Exception as e:
                print(f"Error loading board from file: {e}")
                self.board = [[0 for _ in range(width)] for _ in range(height)]
        elif randomize:
            self.board = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
        else:
            self.board = [[0 for _ in range(width)] for _ in range(height)]

    def _normalize_board_dimensions(self):
        for row in self.board:
            if len(row) < self.width:
                row.extend([0] * (self.width - len(row))) # Pad shorter rows with dead cells

    def load_board_from_file(self, file_path):
        with open(file_path, 'r') as file:
            board_string = file.read()
        return self.load_board(board_string)

    @staticmethod
    def load_board(board_string):
        board = []
        for line in board_string.split('\n'):
            board.append([1 if char == 'X' else 0 for char in line])
        return board

    def update_board(self):
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                new_board[y][x] = self._check_cell(x, y)
        self.board = new_board

    def _check_cell(self, x, y):
        live_neighbors = 0
        for j in range(-1, 2):
            for i in range(-1, 2):
                if not (j == 0 and i == 0):
                    ny, nx = (y + j) % self.height, (x + i) % self.width
                    if self.board[ny][nx]:
                        live_neighbors += 1

        if self.board[y][x]:
            return 1 if live_neighbors == 2 or live_neighbors == 3 else 0
        else:
            return 1 if live_neighbors == 3 else 0

