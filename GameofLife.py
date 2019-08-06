import math
import random
import time
import timeit
import pygame
from pygame.locals import *
import numpy as np
from scipy import signal
from scipy import ndimage
from distutils.core import setup
from Cython.Build import cythonize

print("Starting init...\n")
time_init_start = time.time()

setup(ext_modules=cythonize("cython_iterator.pyx"), include_dirs=[np.get_include()])
import cython_iterator as cy

print("Cython build complete... {:.0f}ms".format((time.time() - time_init_start)*1000))

RED, GREEN, BLUE = (255, 0, 0), (0, 128, 0), (0, 0, 255)
BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)

ON_COLOR = BLACK
OFF_COLOR = WHITE
SCREEN_W, SCREEN_H = 1920, 1080
TOROIDAL_ENV = True
P_0 = 0.5
SCALE = 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), depth=8)
screen.set_alpha(None)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR]+[GRAY]+[RED]+[GREEN]+[BLUE])

BOARD_W, BOARD_H = (0, 2)[TOROIDAL_ENV] + SCREEN_W // SCALE, (0, 2)[TOROIDAL_ENV] + SCREEN_H // SCALE
board_c = np.ascontiguousarray(np.random.choice(a=[0, 1], size=(2, BOARD_W, BOARD_H), p=[1 - P_0, P_0]), dtype=np.uint8)

def step_toroidal_moore_cy():
    #if TOROIDAL_ENV:
    #    board_0[0, :] = board_0[-2, :]
    #    board_0[-1, :] = board_0[1, :]
    #    board_0[:, -1] = board_0[:, 1]
    #    board_0[:, 0] = board_0[:, -2]
    cy.iterate(board_c, c_frame_n)


def draw_board():
    # # # Some sort of buffer thing going on, double flipping makes a huge visual difference in fluidity
    # # Actually its probably just some sort of resonance between simulated FPS and monitor refresh-rate
    # # # Get screen pixels as arr, xor with disp arr or board or whatever, draw points that changed?
    # # Only manage ~3k pixels with draw rects for the cost of blit_arr(1920*1080)
    # # Pixelarray would just be even slower than blit_array?
    # Only if every single pixel is changed?
    # disp_arr = (board_0, board_0[1:-1, 1:-1])[TOROIDAL_ENV]
    active_layer = c_frame_n % 2
    disp_arr = (board_c[active_layer, :, :], board_c[active_layer, 1:-1, 1:-1])[TOROIDAL_ENV]
    pygame.surfarray.blit_array(screen, disp_arr if SCALE == 1 else
                                np.repeat(np.repeat(disp_arr, SCALE, axis=0), SCALE, axis=1))
    pygame.display.update()


def profile_function(function, n_trials=3, n_per_trial=10):
    times = timeit.repeat(setup="from __main__ import " + function, stmt=function+"()",
                          repeat=n_trials, number=n_per_trial)
    print("Frame {:3d} : {:24s} ~{:.2f}ms".format(c_frame_n, function + "()", 1000 * min(times) / n_per_trial))


def empty_region_print(max_window_w):
    print("Empty NxN Ratios:")
    active_layer = c_frame_n % 2
    wide_count = board_c[active_layer, 1:-1, 1:-1].copy()
    empty_ratio = np.bincount(wide_count.ravel())[0] / ((BOARD_W - 1) * (SCREEN_H - 1))
    print("\t 3x3\t{:.2f}".format(empty_ratio))
    for window_w in range(5, max_window_w+1, 2):
        wide_count[:, 1:-1] += wide_count[:, :-2] + wide_count[:, 2:]
        wide_count[1:-1, :] += wide_count[:-2, :] + wide_count[2:, :]
        empty_ratio = np.bincount(np.asarray([wide_count != 0]).ravel())[0]\
            / ((BOARD_W - (window_w // 2)) * (SCREEN_H - (window_w // 2)))
        print("\t{:2d}x{:<2d}\t{:.2f}".format(window_w, window_w, empty_ratio))


def status_print(frame_n: int) -> None:
    global time_chunk_start
    print("F={:<4d}\tT={:.0f}s\t".format(frame_n, (time.time() - time_start)), end="")
    s_per_frame = (time.time() - time_chunk_start) / (required_frames // num_reports)
    print("Avg.t={:.2f}ms\t".format(1000 * s_per_frame), end="")
    print("Avg.FPS={:.0f}".format(1/s_per_frame))
    time_chunk_start = time.time()
    # empty_region_print(269)


def generate_frame():
    global c_frame_n
    flag = c_frame_n % 2
    cy.iterate(board_c, flag)
    pygame.surfarray.blit_array(screen, board_c[flag, 1:-1, 1:-1])
    pygame.display.update()
    status_print(c_frame_n) if c_frame_n % (required_frames // num_reports) == 0 else None
    c_frame_n += 1


c_frame_n = 1
required_frames = 10000
num_reports = 20

time_init_end = time.time()
print("Total Initialization...  {:.0f}ms".format(1000 * (time_init_end - time_init_start)))
print("\nCore-loop clock starting...")
time_chunk_start = time.time()
time_start = time.time()
done = False
while not done and not c_frame_n > required_frames:
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # completed_frames = generate_frame(completed_frames)
    generate_frame()
    clock.tick()

c_frame_n -= 1
time_end = time.time()
print("Core-loop clock stopped...\n")
print("Runtime {:.0f}s".format(time_end - time_start))
print("#Frames ", c_frame_n)
print("Avg. {:.2f}ms Frametime".format(1000 * (time_end - time_start) / c_frame_n))
print("Avg. {:.2f}FPS".format(c_frame_n / (time_end - time_start)))
print("\nExiting...")
