# This is the main file to start the game
# You may add any additional modules and other files you wish

import pygame
import sys
from random import randint
from game import GameOfLife
from board_loader import load_board

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 608
CELL_SIZE = 16

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

ALIVE_COLOR = WHITE
DEAD_COLOR = BLACK

def draw_button(screen, surface, rect, color, text, font_size=50, color_text=BLACK):
    surface.fill(color)
    screen.blit(surface, rect)
    font = pygame.font.Font('ka1.ttf', font_size)
    text_surface = font.render(text, True, color_text)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def show_start_screen(screen, font):
    background_image = pygame.image.load('background_image_1.png')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True
    show_image = False
    while running:
        screen.blit(background_image, (0, 0))

        start_button_surface = pygame.Surface((250, 70))
        start_button_rect = start_button_surface.get_rect(center=(400, 225))
        exit_button_surface = pygame.Surface((200, 70))
        exit_button_rect = exit_button_surface.get_rect(center=(400, 325))
        keyshorts_button_surface = pygame.Surface((450, 70))
        keyshorts_button_rect = keyshorts_button_surface.get_rect(center=(400, 425))

        start_button_color = (134,243,32,255)
        exit_button_color = (236,17,48,255)
        keyshorts_button_color = (254,137,47,255)

        font = pygame.font.Font('ka1.ttf', 75)
        main_text = font.render("Game of Life", True, BLACK)
        main_text_rect = main_text.get_rect(center=(400, 100))
        screen.blit(main_text, main_text_rect)

        draw_button(screen, start_button_surface, start_button_rect, start_button_color, "Start", color_text=BLACK)
        draw_button(screen, keyshorts_button_surface, keyshorts_button_rect, keyshorts_button_color, "Key Commands", font_size=40, color_text=BLACK)
        draw_button(screen, exit_button_surface, exit_button_rect, exit_button_color, "Exit", color_text=BLACK)

        key_shorts_table = pygame.image.load('key_commands.png')
        key_shorts_table = pygame.transform.scale(key_shorts_table, (WINDOW_WIDTH, WINDOW_HEIGHT))
        key_shorts_table_rect = key_shorts_table.get_rect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return True
                if exit_button_rect.collidepoint(event.pos):
                    return False
                if keyshorts_button_rect.collidepoint(event.pos) and not show_image:
                    show_image = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = True
                    show_image = False
                
        if show_image:
            screen.blit(key_shorts_table, key_shorts_table_rect)

        pygame.display.update()

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_board(screen, game):
    for y in range(game.board.shape[0]):
        for x in range(game.board.shape[1]):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game.board[y, x] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, rect)
            else:
                pygame.draw.rect(screen, DEAD_COLOR, rect)

def save_board_to_file(game, file_path):
    with open(file_path, 'w') as file:
        for row in game.board:
            line = ''.join(['X' if cell == 1 else '.' for cell in row])
            file.write(line + '\n')

def main():
    global ALIVE_COLOR
    global DEAD_COLOR
    
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("klaudusia's Game of Life")
    font = pygame.font.SysFont(None, 55)
    
    game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True)
    in_start_screen = True
    paused = False
    speed = 10  # Speed of the game

    while True:
        if in_start_screen:
            start_game = show_start_screen(screen, font)
            if not start_game:
                break
            in_start_screen = False
        else:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:  # Change cell color
                        ALIVE_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))
                    elif event.key == pygame.K_b:  # Change background color
                        DEAD_COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))
                    elif event.key == pygame.K_w:  # Reset colors to default
                        ALIVE_COLOR = WHITE
                        DEAD_COLOR = BLACK
                    elif event.key == pygame.K_s:  # Save game state
                        save_board_to_file(game, 'saved_game.txt') 
                    elif event.key == pygame.K_l:  # Load game state
                        game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, file_path="saved_game.txt")
                    elif event.key == pygame.K_UP:   # Increase speed
                        speed += 5
                    elif event.key == pygame.K_DOWN:  # Decrease speed
                        speed = max(5, speed - 5)
                    elif event.key == pygame.K_r:  # Randomize board
                        game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True)
                    elif event.key == pygame.K_p:  # Pause or resume the game
                        paused = not paused
                    elif event.key == pygame.K_1:  # Load board from file - glider
                        file_path = 'sample_patterns/glider.txt'
                        board = load_board(file_path)
                        if board:
                            game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, file_path=file_path)
                    elif event.key == pygame.K_2:  # Load board from file S- gosper glider gun
                        file_path = 'sample_patterns/gosper-glider-gun.txt'  
                        board = load_board(file_path)
                        if board:
                            game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, file_path=file_path)
                    elif event.key == pygame.K_3:  # Load board from file - pulsar
                        file_path = 'sample_patterns/pulsar.txt'
                        board = load_board(file_path)
                        if board:
                            game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, file_path=file_path)
                    elif event.key == pygame.K_ESCAPE:  # Return to the start screen
                            in_start_screen = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    cell_x, cell_y = mouse_pos[0] // CELL_SIZE, mouse_pos[1] // CELL_SIZE

                    if event.button == 1:  # Left mouse
                        game.board[cell_y][cell_x] = 1  # Add cell
                    elif event.button == 3:  # Right mouse
                        game.board[cell_y][cell_x] = 0  # Remove cell
            
            draw_board(screen, game)
            draw_grid(screen)

            if not paused:
                game.update_board()

            pygame.display.flip()
            clock.tick(speed) # Controls the speed

if __name__ == "__main__":
    main()
