def load_board(file_path):
    board = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                board_line = [1 if char == 'X' else 0 for char in line.strip()]
                board.append(board_line)
        return board
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
