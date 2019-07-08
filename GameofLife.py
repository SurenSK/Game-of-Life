import pygame
import random
import math
import numpy as np
from scipy import signal

BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
GRID_COLOR = GRAY
OFF_COLOR = WHITE
ON_COLOR = BLACK
#BOARD_WIDTH, BOARD_HEIGHT = 961, 961
BOARD_WIDTH, BOARD_HEIGHT = 1920, 1080
CELL_WIDTH, CELL_HEIGHT = 1, 1
#CELL_WIDTH, CELL_HEIGHT = 5, 5
BUFFER_SIZE = 0
N_X = math.floor((BOARD_WIDTH-BUFFER_SIZE)/(CELL_WIDTH+BUFFER_SIZE))
N_Y = math.floor((BOARD_HEIGHT-BUFFER_SIZE)/(CELL_HEIGHT+BUFFER_SIZE))
TOT_CELL_W = BUFFER_SIZE + CELL_WIDTH
TOT_CELL_H = BUFFER_SIZE + CELL_HEIGHT

pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
clock = pygame.time.Clock()

board = [[random.randint(0, 1) == 1 for x in range(N_X)] for y in range(N_Y)]

# a_cell = pygame.image.load("active_cell.png").convert()
a_cell = pygame.image.load("active_cell_min.png").convert()
board_numpy = np.random.choice(a=[0, 1], size=(N_X, N_Y))
n_neighbors = np.empty(shape=(N_X, N_Y), dtype=np.dtype(np.int8))
kernel = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])


def board_print(_board: list) -> None:
    # ~0ms to concatenate & print once for 961x961 board w/ 5x5 cell w/ 1 buffer
    # ~66ms to print each character separately for 961x961 board w/ 5x5 cell w/ 1 buffer
    board_state = ""
    for x in range(N_X):
        for y in range(N_Y):
            board_state += str(_board[x][y] is True)
            # print(_board[x][y], sep='', end='')
        # board_state += "\r\n"
        # print("")
    # board_state += "-" * N_X
    # print("-" * N_X)
    print(board_state)


def simulate_flat_moore(old_board: list) -> list:
    # Just cuts off at board edges
    new_board = [[0 for x in range(N_X)] for y in range(N_Y)]
    for x in range(N_X):
        for y in range(N_Y):
            neighbors = []
            [[neighbors.append(old_board[xx][yy]) if (not(xx == x and yy == y)) else None
              for xx in range(max(x-1, 0), min(x+2, N_X))]
             for yy in range(max(y-1, 0), min(y+2, N_Y))]
            n = sum(neighbors) * (1, -1)[old_board[x][y] == 0]
            new_board[x][y] = 1 if n_neighbors == -3 or n_neighbors == 2 or n_neighbors == 3 else 0
    return new_board


def simulate_toroidal_moore(old_board: list) -> list:
    # Wrap-around / Toriodal Topography
    new_board = [[False for var in range(N_X)] for y in range(N_Y)]
    for x in range(N_X):
        col_x = BUFFER_SIZE + (TOT_CELL_W * x)
        neg_x = x - 1
        pos_x = (x + 1) % N_X
        for y in range(N_Y):
            pos_y = (y + 1) % N_Y
            neg_y = y - 1
            active_neighbors = old_board[x][neg_y] + old_board[x][pos_y] + \
                old_board[neg_x][neg_y] + old_board[neg_x][y] + old_board[neg_x][pos_y] + \
                old_board[pos_x][neg_y] + old_board[pos_x][y] + old_board[pos_x][pos_y]

            if active_neighbors < 2:
                continue
            elif active_neighbors > 3:
                continue
            elif active_neighbors == 3:
                new_board[x][y] = True
                screen.blit(a_cell, (col_x, BUFFER_SIZE + (TOT_CELL_H * y)))
            elif old_board[x][y] is True:
                new_board[x][y] = True
                screen.blit(a_cell, (col_x, BUFFER_SIZE + (TOT_CELL_H * y)))
    return new_board


def numpy_toroidal_moore():
    global n_neighbors, board_numpy
    n_neighbors = signal.convolve2d(board_numpy, kernel, mode='same', boundary='wrap')
    board_numpy[n_neighbors != 2] = 0
    board_numpy[n_neighbors == 3] = 1


done = False
tot_fps = 0
n_frames = 0
tot_frames = 1000
while not done:
    done = n_frames == tot_frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(OFF_COLOR)
    numpy_toroidal_moore()
    # for (x, y) in np.argwhere(board_numpy == 1):
    #    screen.blit(a_cell, (BUFFER_SIZE + (TOT_CELL_W * x), BUFFER_SIZE + (TOT_CELL_H * y)))
    pygame.display.flip()
    tot_fps += clock.get_fps()
    n_frames += 1
    print(clock.get_fps())
    clock.tick()

print("Avg FPS", tot_fps / tot_frames)
print("RunTime", (tot_frames*tot_frames) / tot_fps)
print("Exiting...")
