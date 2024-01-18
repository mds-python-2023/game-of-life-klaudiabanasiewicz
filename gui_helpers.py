from constants import *
import pygame

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

def show_middle_screen(screen, font):
    background_image = pygame.image.load('background_image_1.png')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True
    in_start_screen = False
    while running:
        screen.blit(background_image, (0, 0))

        normal_rules_button_surface = pygame.Surface((450, 70))
        normal_rules_button_rect = normal_rules_button_surface.get_rect(center=(400, 225))
        custom_rules_button_surface = pygame.Surface((450, 70))
        custom_rules_button_rect = custom_rules_button_surface.get_rect(center=(400, 325))
        back_button_surface = pygame.Surface((200, 70))
        back_button_rect = back_button_surface.get_rect(center=(400, 425))

        normal_rules_button_color = (134,243,32,255)
        custom_rules_button_color = (254,137,47,255)
        back_button_color = (236,17,48,255)

        draw_button(screen, normal_rules_button_surface, normal_rules_button_rect, normal_rules_button_color, "Normal Rules", color_text=BLACK)
        draw_button(screen, custom_rules_button_surface, custom_rules_button_rect, custom_rules_button_color, "Custom Rules", font_size=40, color_text=BLACK)
        draw_button(screen, back_button_surface, back_button_rect, back_button_color, "Back", color_text=BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if normal_rules_button_rect.collidepoint(event.pos):
                    return True
                if custom_rules_button_rect.collidepoint(event.pos):
                    return True
                if back_button_rect.collidepoint(event.pos) and not in_start_screen:
                    in_start_screen = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_start_screen = True

        pygame.display.update()