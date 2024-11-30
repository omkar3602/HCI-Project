import pygame
import random
from constants import s_width, s_height, BG_COLOR, GAME_NAME
import cv2
from game import Game
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
        game.draw_text_center(GAME_NAME, 60, (255, 255, 255), window, s_width // 2, s_height // 4)
        game.draw_text_center('Press any key to begin.', 40, (255, 255, 255), window, s_width // 2, (s_height // 2) + 50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                cap = cv2.VideoCapture(0)
                game.gameloop(window, cap)
    pygame.quit()


pygame.init()

window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption(GAME_NAME)

main_menu()  # start game





