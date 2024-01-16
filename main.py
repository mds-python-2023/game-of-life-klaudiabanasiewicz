# This is the main file to start the game
# You may add any additional modules and other files you wish

from logic import *
from gui import *

def main():
    game = GameOfLife()
    view = GameOfLifeView(game)
    view.run()

if __name__ == "__main__":
    main()


