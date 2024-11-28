import pygame
import random
from shapes import shapes, shape_colors
from piece import Piece
import cv2
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# 0) Constants
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

# 1) Game display
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

# 1) Game display
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# 1) Game display
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# 2) Game logic
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# 2) Game logic
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))

# 1) Game display
def draw_text_center(text, size, color, surface, x, y):
    font = pygame.font.SysFont(FONT, size, bold=False)
    label = font.render(text, 1, color)

    surface.blit(label, (x - (label.get_width() / 2), y - (label.get_height() / 2)))

# 1) Game display
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (255, 255, 255), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (255, 255, 255), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

# 1) Game display and 2) Game logic 
def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

# 1) Game display 
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont(FONT, 40)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = (s_width // 2) + (s_width // 16)
    sy = (s_height // 2) + 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, ((sx-10) + j*30, (sy+10) + i*30, 30, 30), 0)

    surface.blit(label, (sx, sy))

# 1) Game display 
def print_score(score, surface):
    font = pygame.font.SysFont(FONT, 40)
    label = font.render('Score: ', 1, (255,255,255))
    
    score_font = pygame.font.SysFont(FONT, 60, bold=False)
    score_label = score_font.render(str(score), 1, (255,255,255))

    sx = (s_width // 2) + (s_width // 3.25)
    sy = (s_height // 2) + 100
    
    surface.blit(label, (sx, sy))
    surface.blit(score_label, (sx+label.get_width()//3, sy+70))

# 1) Game display 
cap = cv2.VideoCapture(0)
def display_camera(surface):
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        # Resize the frame to fit the window
        # This is inverted because the frame is transposed (height, width)
        frame = cv2.resize(frame, ((s_height // 2)-70, (s_width // 2)-70))
        # Flip the frame so that it is not mirrored
        frame = cv2.flip(frame, 0)
        

        frame_surface = pygame.surfarray.make_surface(frame)
        
        sx = (s_width // 2)
        sy = 100

        surface.blit(frame_surface, (sx, sy))

# 1) Game display 
def draw_window(surface):
    surface.fill(BG_COLOR)
    # Tetris Title
    font = pygame.font.SysFont(FONT, 60)
    label = font.render(GAME_NAME, 1, (255,255,255))

    surface.blit(label, (s_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    global grid

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
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
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    score += 1
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            inc = clear_rows(grid, locked_positions)
            if inc > 0:
                score += (inc * 100)

        draw_window(window)
        draw_next_shape(next_piece, window)
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





