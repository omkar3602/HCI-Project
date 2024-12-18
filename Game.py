import pygame
from shapes import shapes, shape_colors
from constants import s_width, s_height, play_width, play_height, top_left_x, top_left_y, FONT_PATH, BG_COLOR, GAME_NAME
from block import Block
import cv2
import random
from vision import get_gestures

class Game:
    def gameloop(self, window, cap):
        global grid

        locked_positions = {}
        grid = self.create_grid(locked_positions)

        change_block = False
        run = True
        current_block = self.get_shape()
        next_block = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        score = 0
        left_wait = 0
        right_wait = 0
        rotate_wait = 0
        down_wait = 0
        command = ''
        
        while run:
            grid = self.create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick(15)

            # PIECE FALLING CODE
            if fall_time/1000 >= fall_speed:
                fall_time = 0
                current_block.y += 1
                if not (self.valid_space(current_block, grid)) and current_block.y > 0:
                    current_block.y -= 1
                    change_block = True

            gesture = get_gestures(cap)
            if gesture == 'left':
                left_wait += 1
            elif gesture == 'right':
                right_wait += 1
            elif gesture == 'rotate':
                rotate_wait += 1
            elif gesture == 'down':
                down_wait += 1
            
            WAIT_TIME = 6
            if left_wait >= WAIT_TIME:
                command = 'LEFT'
                current_block.x -= 1
                if not self.valid_space(current_block, grid):
                    current_block.x += 1
                left_wait = 0
                right_wait = 0
                rotate_wait = 0
                down_wait = 0
            elif right_wait >= WAIT_TIME:
                command = 'RIGHT'
                current_block.x += 1
                if not self.valid_space(current_block, grid):
                    current_block.x -= 1
                left_wait = 0
                right_wait = 0
                rotate_wait = 0
                down_wait = 0
            elif rotate_wait >= WAIT_TIME + 4:
                command = 'ROTATE'
                current_block.rotation = current_block.rotation + 1 % len(current_block.shape)
                if not self.valid_space(current_block, grid):
                    current_block.rotation = current_block.rotation - 1 % len(current_block.shape)
                left_wait = 0
                right_wait = 0
                rotate_wait = 0
                down_wait = 0
            elif down_wait >= WAIT_TIME:
                command = 'DOWN'
                score += 1
                current_block.y += 1
                if not self.valid_space(current_block, grid):
                    current_block.y -= 1
                left_wait = 0
                right_wait = 0
                rotate_wait = 0
                down_wait = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        current_block.x -= 1
                        if not self.valid_space(current_block, grid):
                            current_block.x += 1

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        current_block.x += 1
                        if not self.valid_space(current_block, grid):
                            current_block.x -= 1
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        # rotate shape
                        current_block.rotation = current_block.rotation + 1 % len(current_block.shape)
                        if not self.valid_space(current_block, grid):
                            current_block.rotation = current_block.rotation - 1 % len(current_block.shape)

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        score += 1
                        # move shape down
                        current_block.y += 1
                        if not self.valid_space(current_block, grid):
                            current_block.y -= 1

            shape_pos = self.convert_shape_format(current_block)

            # add block to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_block.color

            # IF BLOCK HITS THE GROUND
            if change_block:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_block.color
                current_block = next_block
                next_block = self.get_shape()
                change_block = False

                inc = self.clear_rows(grid, locked_positions)
                if inc > 0:
                    score += (inc * 100)

            self.draw_window(window, grid)
            self.draw_next_shape(next_block, window)
            self.print_score(score, window)
            self.display_camera(window, cap)
            self.display_command(window, command)
            pygame.display.update()

            # Check if user lost
            if self.check_lost(locked_positions):
                run = False

        # Remove the game, camera and score from the screen
        window.fill(BG_COLOR)
        self.draw_text_center('Game Over', 100, (255,255,255), window, s_width // 2, (s_height // 2) - 100)
        self.draw_text_center('Score: ' + str(score), 60, (255,255,255), window, s_width // 2, s_height // 2)
        pygame.display.update()
        pygame.time.delay(5000)


    def create_grid(self, locked_positions={}):
        grid = [[(0,0,0) for x in range(10)] for x in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape):
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

    def valid_space(self, shape, grid):
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
        return True


    def draw_text_center(self, text, size, color, surface, x, y):
        font = pygame.font.Font(FONT_PATH, size)
        label = font.render(text, 1, color)

        surface.blit(label, (x - (label.get_width() / 2), y - (label.get_height() / 2)))

    def draw_grid(self, surface, row, col):
        sx = top_left_x
        sy = top_left_y
        for i in range(row):
            pygame.draw.line(surface, (255, 255, 255), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
            for j in range(col):
                pygame.draw.line(surface, (255, 255, 255), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

    def draw_next_shape(self, shape, surface):
        font = pygame.font.Font(FONT_PATH, 30)
        label = font.render('Next Shape', 1, (255,255,255))

        sx = (s_width // 2) + (s_width // 16)
        sy = (s_height // 2) + 150
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, ((sx-10) + j*30, (sy+10) + i*30, 30, 30), 0)

        surface.blit(label, (sx, sy))

    def print_score(self, score, surface):
        font = pygame.font.Font(FONT_PATH, 30)
        label = font.render('Score: ', 1, (255,255,255))
        
        score_font = pygame.font.Font(FONT_PATH, 50)
        score_label = score_font.render(str(score), 1, (255,255,255))

        sx = (s_width // 2) + (s_width // 3.25)
        sy = (s_height // 2) + 150
        
        surface.blit(label, (sx, sy))
        surface.blit(score_label, (sx+label.get_width()//3, sy+70))

    def display_command(self, surface, command):
        command_font = pygame.font.Font(FONT_PATH, 50)
        command_label = command_font.render(command, 1, (255,255,255))

        sx = (s_width // 2) + (s_width // 5) - (command_label.get_width()//2)
        sy = (s_height // 2) + 50
        surface.blit(command_label, (sx, sy))

    def display_camera(self, surface, cap):
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

    def draw_window(self, surface, grid):
        surface.fill(BG_COLOR)
        # Tetris Title
        font = pygame.font.Font(FONT_PATH, 50)
        label = font.render(GAME_NAME, 1, (255,255,255))

        surface.blit(label, (s_width / 2 - (label.get_width() / 2), 20))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

        # draw grid and border
        self.draw_grid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):
        global shapes, shape_colors

        return Block(5, 0, random.choice(shapes))

    def clear_rows(self, grid, locked):
        # need to see if row is clear then shift every other row above down one
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
