import math
import random
import time
import timeit
import pygame
import numpy as np
from scipy import signal
from scipy import ndimage

RED, GREEN, BLUE = (255, 0, 0), (0, 128, 0), (0, 0, 255)
BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)

ON_COLOR = BLACK
OFF_COLOR = WHITE
BOARD_W, BOARD_H = 1920, 1080
SCALE = 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_W, BOARD_H), depth=8)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR]+[BLUE]+[GREEN]+[RED])

CELLS_W, CELLS_H = BOARD_W // SCALE, BOARD_H // SCALE
board = np.random.choice(a=[0, 1], size=(CELLS_W+2, CELLS_H+2))
n_neighbors = np.zeros(shape=(CELLS_W+2, CELLS_H+2), dtype=np.dtype(np.int8))


def step_toroidal_moore():
    global n_neighbors, board
    board[0, :] = board[-2, :]
    board[:, 0] = board[:, -2]
    board[-1, :] = board[1, :]
    board[:, -1] = board[:, 1]
    n_neighbors[:, 1:-1] = board[:, :-2] + board[:, 2:] + board[:, 1:-1]
    n_neighbors[1:-1, :] += n_neighbors[:-2, :] + n_neighbors[2:, :] - board[1:-1, :]
    board[n_neighbors != 2] = 0
    board[n_neighbors == 3] = 1


def draw_board():
    board_c = board[1:-1, 1:-1] if SCALE == 1 else np.repeat(np.repeat(board[1:-1, 1:-1], SCALE, axis=0), SCALE, axis=1)
    pygame.surfarray.blit_array(screen, board_c)
    pygame.display.flip()


def status_print(c_frame_n: int, frequency: int) -> None:
    if c_frame_n % frequency == 0:
        print("{:.1f}ms Avg.Frametime over {:4d} Frames\t\tRuntime: {:6.3f}s"
              .format((1000 * (time.time() - time_start) / c_frame_n), c_frame_n, (time.time() - time_start)))


def profile_function(function, n_trials=3, n_per_trial=10):
    times = timeit.repeat(setup="from __main__ import " + function, stmt=function + "()",
                          repeat=n_trials, number=n_per_trial)
    print("Frame {:3d} : {:24s} ~{:.2f}ms".format(frame_n, function+"()", 1000 * min(times)/n_per_trial))


def step_frame():
    global frame_n
    frame_n += 1
    # step_toroidal_moore()
    step_toroidal_moore()
    # profile_function("draw_board")
    draw_board()
    # status_print(frame_n, 100)


# ~2.5ms overhead
frame_n = 0
required_frames = 999
print("\nStarting clock...")
time_start = time.time()
done = False
while not done:
    done = frame_n > required_frames
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
        # if event.type == pygame.MOUSEBUTTONDOWN:
    step_frame()
    clock.tick()

time_end = time.time()
print("Stopped clock...\n")
print("RunTime ", (time_end - time_start))
print("#Frames ", frame_n)
print("ms per frame ", 1000 * (time_end - time_start) / frame_n)
print("\nExiting...")
