import math
import random
import time
import timeit
import pygame
from pygame.locals import *
import numpy as np
from scipy import signal
from scipy import ndimage

print("Starting init...")
time_init_start = time.time()

import cython_iterator as cy

RED, GREEN, BLUE = (255, 0, 0), (0, 128, 0), (0, 0, 255)
BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)

ON_COLOR = BLACK
OFF_COLOR = WHITE
SCREEN_W, SCREEN_H = 1920, 1080
TOROIDAL_ENV = True
INI_P = 0.5
SCALE = 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), depth=8)
screen.set_alpha(None)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR]+[GRAY]+[RED]+[GREEN]+[BLUE])

BOARD_W, BOARD_H = (0, 2)[TOROIDAL_ENV] + SCREEN_W // SCALE, (0, 2)[TOROIDAL_ENV] + SCREEN_H // SCALE
board = np.random.choice(a=[0, 1], size=(BOARD_W, BOARD_H), p=[1 - INI_P, INI_P])
count = np.zeros(shape=(BOARD_W, BOARD_H), dtype=np.dtype(np.float))


def step_toroidal_moore():
    global count, board
    count = board.copy()
    if TOROIDAL_ENV:
        count[0, :] = count[-2, :]
        count[-1, :] = count[1, :]
        count[:, -1] = count[:, 1]
        count[:, 0] = count[:, -2]
    count[:, 1:-1] += count[:, :-2] + count[:, 2:]
    count[1:-1, :] += count[:-2, :] + count[2:, :]
    board[count != 4] = 0
    board[count == 3] = 1


def step_toroidal_moore_cy():
    global count, board
    if TOROIDAL_ENV:
        count[0, :] = count[-2, :]
        count[-1, :] = count[1, :]
        count[:, -1] = count[:, 1]
        count[:, 0] = count[:, -2]
    count = board.copy()
    board = cy.iterate(board, count)


def draw_board():
    # # # Some sort of buffer thing going on, double flipping makes a huge visual difference in fluidity
    # # # Get screen pixels as arr, xor with disp arr or board or whatever, draw points that changed
    # # # # Only manage ~3k pixels with draw rects for the cost of blit_arr(1920*1080)
    # # # # Pixelarray would just be even slower than blit_array?
    disp_arr = (board, board[1:-1, 1:-1])[TOROIDAL_ENV]
    #pygame.surfarray.blit_array(screen, disp_arr if SCALE == 1 else
    #                            np.repeat(np.repeat(disp_arr, SCALE, axis=0), SCALE, axis=1))
    pygame.surfarray.blit_array(screen, disp_arr)
    pygame.display.update()


def profile_function(function, n_trials=3, n_per_trial=10):
    times = timeit.repeat(setup="from __main__ import " + function, stmt=function+"()",
                          repeat=n_trials, number=n_per_trial)
    print("Frame {:3d} : {:24s} ~{:.2f}ms".format(completed_frames, function+"()", 1000 * min(times)/n_per_trial))


def empty_region_print(max_window_w):
    print("Empty NxN Ratios:")
    wide_count = count.copy()
    empty_ratio = np.bincount(wide_count.ravel())[0] / ((BOARD_W - 1) * (SCREEN_H - 1))
    print("\t 3x3\t{:.2f}".format(empty_ratio))
    for window_w in range(5, max_window_w+1, 2):
        wide_count[:, 1:-1] += wide_count[:, :-2] + wide_count[:, 2:]
        wide_count[1:-1, :] += wide_count[:-2, :] + wide_count[2:, :]
        empty_ratio = np.bincount(np.asarray([wide_count != 0]).ravel())[0]\
            / ((BOARD_W - (window_w // 2)) * (SCREEN_H - (window_w // 2)))
        print("\t{:2d}x{:<2d}\t{:.2f}".format(window_w, window_w, empty_ratio))


def status_print(frame_n: int) -> None:
    print("F={:<4d}\tT={:.0f}s\tAvg.t={:.2f}ms"
          .format(frame_n, (time.time() - time_start), (1000 * (time.time() - time_start) / frame_n)))
    # empty_region_print(269)


def generate_frame(c_frame_n):
    # profile_function("step_toroidal_moore")
    # step_toroidal_moore()
    # profile_function("step_toroidal_moore_cy")
    step_toroidal_moore_cy()
    # profile_function("draw_board")
    draw_board()
    status_print(c_frame_n) if c_frame_n % (required_frames // 20) == 0 else None
    return c_frame_n + 1


completed_frames = 1
required_frames = 1000

time_init_end = time.time()
print("\n{:.0f}ms Initialization".format(1000 * (time_init_end - time_init_start)))
print("\nCore-loop clock starting...")
time_start = time.time()
done = False
while not done and completed_frames < required_frames:
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # completed_frames = generate_frame(completed_frames)

    completed_frames = generate_frame(completed_frames)
    clock.tick()

time_end = time.time()
print("Core-loop clock stopped...\n")
print("Runtime ", (time_end - time_start))
print("#Frames ", completed_frames)
print("Avg. {:.0f}ms Frametime".format(1000 * (time_end - time_start) / completed_frames))
print("Avg. {:.2f}FPS".format(completed_frames / (time_end - time_start)))
print("\nExiting...")
