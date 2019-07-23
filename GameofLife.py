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
INIT_CONCEN = 0.5
SCALE = 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_W, BOARD_H), depth=8)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR]+[BLUE]+[GREEN]+[RED])

CELLS_W, CELLS_H = BOARD_W // SCALE, BOARD_H // SCALE
count = np.zeros(shape=(CELLS_W+2, CELLS_H+2), dtype=np.dtype(np.float))
board = np.random.choice(a=[0, 1], size=(CELLS_W+2, CELLS_H+2), p=[1-INIT_CONCEN, INIT_CONCEN])


def step_toroidal_moore():
    global count
    count = board.copy()
    count[0, :] = count[-2, :]
    count[:, 0] = count[:, -2]
    count[-1, :] = count[1, :]
    count[:, -1] = count[:, 1]
    count[:, 1:-1] += count[:, :-2] + count[:, 2:]
    count[1:-1, :] += count[:-2, :] + count[2:, :]
    board[count != 4] = 0
    board[count == 3] = 1


def draw_board():
    disp_arr = board[1:-1, 1:-1] if SCALE == 1 else \
        np.repeat(np.repeat(board[1:-1, 1:-1], SCALE, axis=0), SCALE, axis=1)
    pygame.surfarray.blit_array(screen, disp_arr)
    pygame.display.flip()


def profile_function(function, n_trials=3, n_per_trial=10):
    times = timeit.repeat(setup="from __main__ import " + function, stmt=function+"()",
                          repeat=n_trials, number=n_per_trial)
    print("Frame {:3d} : {:24s} ~{:.2f}ms".format(completed_frames, function+"()", 1000 * min(times)/n_per_trial))


def status_print(frame_n: int, freq: int) -> None:
    if frame_n % freq == 0:
        print("{:.1f}ms FrameTime over {:4d} Frames\tTotalRuntime: {:6.3f}s"
              .format((1000 * (time.time() - time_start) / frame_n), frame_n, (time.time() - time_start)))
        # print(np.bincount(count.ravel()))


def generate_frame():
    global completed_frames
    # profile_function("draw_board")
    draw_board()
    # profile_function("step_toroidal_moore")
    step_toroidal_moore()
    completed_frames += 1


completed_frames = 0
required_frames = 1000
print("\nCore-loop clock starting...")
time_start = time.time()
done = False
while not done and completed_frames < required_frames:
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # generate_frame()

    generate_frame()
    # status_print(completed_frames, 100)
    # print("{:.0f}".format(clock.get_fps()))
    clock.tick()

time_end = time.time()
print("Core-loop clock stopped...\n")
print("RunTime ", (time_end - time_start))
print("#Frames ", completed_frames)
print("Avg.Frametime ", 1000 * (time_end - time_start) / completed_frames)
print("\nExiting...")
