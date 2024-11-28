import pygame
import random
from constants import s_width, s_height, play_width, play_height, top_left_x, top_left_y, FONT, BG_COLOR, GAME_NAME
from block import Block
import cv2
from game_utils import create_grid, convert_shape_format, valid_space, draw_text_center, draw_grid, draw_window, draw_next_shape, print_score, display_camera, clear_rows, check_lost, get_shape
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""


def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_block = False
    run = True
    current_block = get_shape()
    next_block = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0
    
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 4:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005
            

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_block.y += 1
            if not (valid_space(current_block, grid)) and current_block.y > 0:
                current_block.y -= 1
                change_block = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_block.x -= 1
                    if not valid_space(current_block, grid):
                        current_block.x += 1

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    current_block.x += 1
                    if not valid_space(current_block, grid):
                        current_block.x -= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # rotate shape
                    current_block.rotation = current_block.rotation + 1 % len(current_block.shape)
                    if not valid_space(current_block, grid):
                        current_block.rotation = current_block.rotation - 1 % len(current_block.shape)

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    score += 1
                    # move shape down
                    current_block.y += 1
                    if not valid_space(current_block, grid):
                        current_block.y -= 1

        shape_pos = convert_shape_format(current_block)

        # add block to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_block.color

        # IF PIECE HIT GROUND
        if change_block:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_block.color
            current_block = next_block
            next_block = get_shape()
            change_block = False

            inc = clear_rows(grid, locked_positions)
            if inc > 0:
                score += (inc * 100)

        draw_window(window, grid)
        draw_next_shape(next_block, window)
        print_score(score, window)
        display_camera(window)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_center('You Lost', 40, (255,255,255), window, s_width // 2, s_height // 2)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        window.fill(BG_COLOR)
        draw_text_center(GAME_NAME, 70, (255, 255, 255), window, s_width // 2, s_height // 4)
        draw_text_center('Press any key to begin.', 50, (255, 255, 255), window, s_width // 2, (s_height // 2) + 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game





