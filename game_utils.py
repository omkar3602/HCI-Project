import pygame
from shapes import shapes, shape_colors
from constants import s_width, s_height, play_width, play_height, top_left_x, top_left_y, FONT, BG_COLOR, GAME_NAME
from block import Block
import cv2
import random

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
def draw_window(surface, grid):
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

    return Block(5, 0, random.choice(shapes))

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
