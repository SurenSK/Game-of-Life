import pygame
import random
import math
import time
import numpy as np
from scipy import signal
from scipy import ndimage

BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
GRID_COLOR = GRAY
OFF_COLOR = WHITE
ON_COLOR = BLACK
BOARD_W, BOARD_H = 1920, 1080
CELL_W, CELL_H, BUFFER = 1, 1, 0
# BOARD_W, BOARD_H = 961, 961
# CELL_W, CELL_H, BUFFER = 5, 5, 1
N_X = math.floor((BOARD_W - BUFFER) / (CELL_W + BUFFER))
N_Y = math.floor((BOARD_H - BUFFER) / (CELL_H + BUFFER))

pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_W, BOARD_H), depth=8)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR])
clock = pygame.time.Clock()
img = pygame.Surface(screen.get_size())

# a_cell = pygame.image.load("active_cell.png").convert()
a_cell = pygame.image.load("active_cell_min.png").convert()

TILE_COORDS = [[(BUFFER+((BUFFER+CELL_W) * x), BUFFER+((BUFFER+CELL_H) * y)) for y in range(N_Y)] for x in range(N_X)]
board = [[random.randint(0, 1) == 1 for x in range(N_X)] for y in range(N_Y)]

board_numpy = np.random.choice(a=[0, 1], size=(N_X, N_Y))
n_neighbors = np.zeros(shape=(N_X, N_Y), dtype=np.dtype(np.int8))
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
        col_x = BUFFER + ((BUFFER + CELL_W) * x)
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
                screen.blit(a_cell, (col_x, BUFFER + ((BUFFER + CELL_H) * y)))
            elif old_board[x][y] is True:
                new_board[x][y] = True
                screen.blit(a_cell, (col_x, BUFFER + ((BUFFER + CELL_H) * y)))
    return new_board


def numpy_toroidal_moore():
    global n_neighbors, board_numpy
    # n_neighbors = signal.convolve2d(board_numpy, kernel, mode='same', boundary='wrap')

    kernel_h = np.array([1, 1, 1])
    n_neighbors = ndimage.convolve1d(ndimage.convolve1d(board_numpy, kernel_h, axis=0, mode="wrap"), kernel_h, axis=1, mode="wrap") - board_numpy
    board_numpy[n_neighbors != 2] = 0
    board_numpy[n_neighbors == 3] = 1


def draw_board():
    pygame.surfarray.blit_array(screen, board_numpy)
    pygame.display.flip()


def status_print(c_frame_n: int, frequency: int) -> None:
    if c_frame_n % frequency == 0:
        print("{:.3f}s Runtime, {:.0f}FPS Avg. over {:d} Frames".
              format((time.time() - time_start), (c_frame_n / (time.time() - time_start)), c_frame_n))


done = False
frame_n = 0
required_frames = 1000

print("\nStarting clock...")
time_start = time.time()
while not done:
    frame_n += 1
    done = frame_n == required_frames
    for event in pygame.event.get():
            done = True if event.type == pygame.QUIT else False

    numpy_toroidal_moore()
    draw_board()
    # status_print(frame_n, 100)
    clock.tick()

time_end = time.time()
print("Stopped clock...\n")
print("RunTime ", (time_end - time_start))
print("#Frames ", frame_n)
print("ms per frame ", 1000 * (time_end - time_start) / frame_n)
print("\nExiting...")
