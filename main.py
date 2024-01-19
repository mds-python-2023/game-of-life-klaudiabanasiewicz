# This is the main file to start the game
# You may add any additional modules and other files you wish

import pygame
import sys
from random import randint
from game import GameOfLife
from board_loader import load_board, save_board_to_file
from gui_helpers import *
from constants import *

def draw_board(screen, game):
    for y in range(game.board.shape[0]):
        for x in range(game.board.shape[1]):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game.board[y, x] == 1:
                pygame.draw.rect(screen, ALIVE_COLOR, rect)
            else:
                pygame.draw.rect(screen, DEAD_COLOR, rect)

START_SCREEN = 1
MIDDLE_SCREEN = 2
GAME = 3
INPUT_BOX = 4
CUSTOM_GAME = 5

def main():
    global ALIVE_COLOR
    global DEAD_COLOR
    
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("klaudusia's Game of Life")
    font = pygame.font.Font('ka1.ttf', 50)

    current_state = START_SCREEN
    game = None
    paused = False
    speed = 10
    
    while True:
        if current_state == START_SCREEN:
            action = show_start_screen(screen, font)
            if action == 'start':
                current_state = MIDDLE_SCREEN
            elif action == 'exit':
                break

        elif current_state == MIDDLE_SCREEN:
            action = show_middle_screen(screen, font)
            if action == 'back':
                current_state = START_SCREEN
            elif action == 'normal_rules':
                current_state = GAME
            elif action == 'custom_rules':
                current_state = INPUT_BOX
        
        elif current_state == INPUT_BOX:
            action, custom_survival_rules, custom_birth_rules = input_box(screen, font)
            if action == 'back':
                current_state = MIDDLE_SCREEN
            if action == "custom_game":
                current_state = CUSTOM_GAME

        elif current_state == GAME or current_state == CUSTOM_GAME:
            if game is None:  # Initialize the game if not already done
                if current_state == GAME:
                    game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True) 
                elif current_state == CUSTOM_GAME:
                    game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True, survival_rules=custom_survival_rules, birth_rules=custom_birth_rules) 
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
                        if current_state == GAME:
                            game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True) 
                        elif current_state == CUSTOM_GAME:
                            game = GameOfLife(WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE, randomize=True, survival_rules=custom_survival_rules, birth_rules=custom_birth_rules) 
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
                            current_state = MIDDLE_SCREEN
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
            
    pygame.quit()

if __name__ == "__main__":
    main()
