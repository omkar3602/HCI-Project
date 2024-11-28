import pygame
import random
from constants import s_width, s_height, play_width, play_height, top_left_x, top_left_y, FONT, BG_COLOR, GAME_NAME
from block import Block
import cv2
from Game import Game
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""


def main_menu():
    run = True
    game = Game()
    while run:
        window.fill(BG_COLOR)
        game.draw_text_center(GAME_NAME, 70, (255, 255, 255), window, s_width // 2, s_height // 4)
        game.draw_text_center('Press any key to begin.', 50, (255, 255, 255), window, s_width // 2, (s_height // 2) + 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                cap = cv2.VideoCapture(0)
                game.gameloop(window, cap)
    pygame.quit()


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game





