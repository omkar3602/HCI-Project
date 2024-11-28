import pygame
pygame.font.init()

# GLOBALS VARS
s_width = 1000
s_height = 700
play_width = 300  # 300 // 10 = 30 width per block
play_height = 600  # 600 // 20 = 20 height per blocck
block_size = 30

top_left_x = 150
top_left_y = s_height - play_height - 20

FONT = pygame.font.get_default_font()
BG_COLOR = (37,37,38,255)
GAME_NAME = 'GESTURE-CONTROLLED TETRIS'