import pygame
import sys
from constants import *

class GameOfLifeView:
    def __init__(self, game_of_life, cell_size=10, screen_width=800, screen_height=600):
        self.game_of_life = game_of_life
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = 'start_screen'  # Initialize the state attribute

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()

    def draw_text(self, text, position, font_size=36):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)

    def draw_button(self, text, position, size, action=None):
        button_rect = pygame.Rect(position, size)
        pygame.draw.rect(self.screen, (180, 180, 180), button_rect)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if action:
                    action()

        self.draw_text(text, (position[0] + 10, position[1] + 10), font_size=24)
        return button_rect

    def draw_board(self):
        print('Starting drawing loop')
        for y in range(self.game_of_life.height):
            for x in range(self.game_of_life.width):
                rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.game_of_life.board[y][x] == 1:
                    pygame.draw.rect(self.screen, WHITE, rect)  # Draw live cell
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)  # Draw dead cell
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)  # Draw cell border
        print('Ending drawing loop')

    def run(self):
        while True:
            self.clock.tick(10)
            self.screen.fill(BLACK)  # Fill the screen with a white background

            if self.state == 'start_screen':
                self.handle_start_screen()
            elif self.state == 'options_screen':
                self.handle_options_screen()
            elif self.state == 'game':
                self.draw_board()
                self.game_of_life.update_board() 
                # Update the board for the next iteration

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()  # Update the entire screen at the end of each frame

    def handle_start_screen(self):
        # Render some text or buttons here to ensure something is displayed
        self.draw_text("Welcome to Game of Life", (100, 100))
        self.draw_button("Start the Game", (300, 250), (200, 50), action=self.start_game)

    def handle_options_screen(self):
        self.draw_button("Randomized Board", (100, 100), (200, 50), action=self.start_randomized)
        self.draw_button("Glider", (100, 200), (200, 50), action=self.start_glider)
        self.draw_button("Gosper Glider Gun", (100, 300), (200, 50), action=self.start_gosper_glider_gun)
        self.draw_button("Pulsar", (100, 400), (200, 50), action=self.start_pulsar)

    def start_game(self):
        self.state = 'options_screen'

    def start_randomized(self):
        self.game_of_life.__init__(randomize=True)
        self.screen = pygame.display.set_mode((300, 300))
        self.state = 'game'

    def start_glider(self):
        self.game_of_life.__init__(file_path='sample_patterns/glider.txt')
        self.screen = pygame.display.set_mode((300, 300))
        self.state = 'game'

    def start_gosper_glider_gun(self):
        self.game_of_life.__init__(file_path='sample_patterns/gosper-glider-gun.txt')
        self.screen = pygame.display.set_mode((300, 300))
        self.state = 'game'

    def start_pulsar(self):
        self.game_of_life.__init__(file_path='sample_patterns/pulsar.txt')
        self.screen = pygame.display.set_mode((300, 300))
        self.state = 'game'
