# This is the main file to start the game
# You may add any additional modules and other files you wish

from logic import *
from gui import *

def main():
    pattern_file_path = "sample_patterns/pulsar.txt"
    game = GameOfLife(file_path=pattern_file_path)
    view = GameOfLifeView(game)
    view.run()

if __name__ == "__main__":
    main()

