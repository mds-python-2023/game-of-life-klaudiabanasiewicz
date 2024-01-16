import random
import pygame

class GameOfLife:
    def __init__(self, width=30, height=30, randomize=False, file_path=None):
        self.width = width
        self.height = height
        # Initialize an empty board of the specified size
        self.board = [[0 for _ in range(width)] for _ in range(height)]

        if file_path:
            pattern = self.load_board_from_file(file_path)
            self.load_board(str(pattern))
            self.place_pattern_in_center(pattern)
            self.adjust_board_size()
        elif randomize:
            self.board = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
        else:
            self.board = [[0 for _ in range(width)] for _ in range(height)]

    def load_board_from_file(self, file_path):
        with open(file_path, 'r') as file:
            board_string = file.read()
        return self.load_board(board_string)

    @staticmethod
    def load_board(board_string):
        board = []
        for line in board_string.splitlines():  # Corrected line splitting
            board.append([1 if char == 'X' else 0 for char in line])
        return board

    def update_board(self):
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.board[y][x] == 1:  # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_board[y][x] = 0  # Cell dies
                    else:
                        new_board[y][x] = 1  # Cell lives
                else:  # Cell is dead
                    if live_neighbors == 3:
                        new_board[y][x] = 1  # Cell becomes alive
        self.board = new_board

    def adjust_board_size(self):
        pattern_height = len(self.board)
        pattern_width = max(len(row) for row in self.board)

        # Determine the new size of the board to make it as square as possible
        new_size = max(pattern_height, pattern_width)

        # Add additional rows if necessary
        for _ in range(new_size - pattern_height):
            self.board.append([0] * pattern_width)

        # Add additional columns to each row if necessary
        for row in self.board:
            row.extend([0] * (new_size - len(row)))

        # Update the width and height attributes
        self.width = new_size
        self.height = new_size


    def place_pattern_in_center(self, pattern):
        pattern_height = len(pattern)
        pattern_width = max(len(row) for row in pattern)

        # Calculate the necessary board size to fit the pattern and be square
        board_size = max(self.width, self.height, pattern_width, pattern_height)
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]

        # Calculate the top left position to start placing the pattern
        start_y = (board_size - pattern_height) // 2
        start_x = (board_size - pattern_width) // 2

        for y in range(pattern_height):
            for x in range(pattern_width):
                self.board[start_y + y][start_x + x] = pattern[y][x]

        # Update the width and height attributes
        self.width = board_size
        self.height = board_size

    def count_live_neighbors(self, x, y):
        live_neighbors = 0
        for j in range(-1, 2):
            for i in range(-1, 2):
                if not (j == 0 and i == 0):
                    ny, nx = (y + j) % self.height, (x + i) % self.width
                    live_neighbors += self.board[ny][nx]
        return live_neighbors
