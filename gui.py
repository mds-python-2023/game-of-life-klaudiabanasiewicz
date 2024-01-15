import pygame
import sys

class GameOfLifeView:
    def __init__(self, game_of_life, cell_size=10, fps=10):
        self.game_of_life = game_of_life
        self.cell_size = cell_size
        self.fps = fps

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.game_of_life.width * self.cell_size, self.game_of_life.height * self.cell_size))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.game_of_life.update_board()
            self.draw_board()
            pygame.display.flip()

    def draw_board(self):
        self.screen.fill(pygame.Color('white'))
        for y in range(self.game_of_life.height):
            for x in range(self.game_of_life.width):
                rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.game_of_life.board[y][x] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('black'), rect)
                pygame.draw.rect(self.screen, pygame.Color('grey'), rect, 1)
