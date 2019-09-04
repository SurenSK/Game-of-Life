import time
import timeit
import pygame
import numpy as np
import ctypes
import sys
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import random
import cProfile

print("Starting init...\n")
time_init_start = time.time()

ext_modules = [Extension("cython_iterator", ["cython_iterator.pyx"],
                         extra_compile_args=["/openmp"],
                         extra_link_args=['/openmp'])]
setup(include_dirs=[np.get_include()], ext_modules=cythonize(ext_modules))
import cython_iterator as cy

print("Cython build complete... {:.0f}ms".format((time.time() - time_init_start)*1000))

RED, GREEN, BLUE = (255, 0, 0), (0, 128, 0), (0, 0, 255)
BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)

ON_COLOR = BLACK
OFF_COLOR = WHITE
SCREEN_W, SCREEN_H = 10000, 10000
TOROIDAL_ENV = True
P_0 = 0.5
SCALE = 1

time_pygame_init_start = time.time()
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), depth=8)
screen.set_alpha(None)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR]+[GRAY]+[RED]+[GREEN]+[BLUE])
print("Pygame setup complete... {:.0f}ms".format((time.time() - time_pygame_init_start)*1000))


BOARD_W, BOARD_H = (0, 2)[TOROIDAL_ENV] + SCREEN_W // SCALE, (0, 2)[TOROIDAL_ENV] + SCREEN_H // SCALE
c_board = np.ascontiguousarray(np.empty((2, BOARD_W, BOARD_H), dtype=np.uint8, order='C'))
time_rand_start = time.time()
cy.set_random(c_board, P_0)
print("Randomization complete.. {:.0f}ms".format((time.time() - time_rand_start)*1000))
# print("\tAlive P_0: {:.1f}%".format(100*np.count_nonzero(c_board)/c_board.size))

count_over_2ms = 0


# def ctypes_test():
#     NUM = 167
#     fun = ctypes.CDLL("some_c.so")
#     fun.myFunction.argtypes = [ctypes.c_int]
#     returnVal = fun.myFunction(NUM)
#     print(returnVal)

# np_board = np.ascontiguousarray(np.empty((BOARD_W, BOARD_H), dtype=np.uint8, order='C'))
# for i in range(BOARD_H):
#     np_board[:, i] = np.ascontiguousarray(np.random.choice(a=[0, 1], size=BOARD_W, p=[1 - P_0, P_0]), dtype=np.uint8)
# np_count = np.ascontiguousarray(np.zeros(shape=(BOARD_W, BOARD_H), dtype=np.dtype(np.uint8)))
# def step_toroidal_moore_np():
#     if TOROIDAL_ENV:
#         np_board[0, :] = np_board[-2, :]
#         np_board[-1, :] = np_board[1, :]
#         np_board[:, -1] = np_board[:, 1]
#         np_board[:, 0] = np_board[:, -2]
#     np_count[:, 1:-1] = np_board[:, :-2] + np_board[:, 2:] + np_board[:, 1:-1]
#     np_count[1:-1, :] += np_count[:-2, :] + np_count[2:, :]
#     np_board[np_count != 4] = 0
#     np_board[np_count == 3] = 1


def step_toroidal_moore_cy():
    if TOROIDAL_ENV:
        c_board[0, :] = c_board[-2, :]
        c_board[-1, :] = c_board[1, :]
        c_board[:, -1] = c_board[:, 1]
        c_board[:, 0] = c_board[:, -2]
    cy.iterate(c_board, c_frame)


def draw_board():
    # # Get screen pixels as arr, xor with disp arr or board or whatever, only draw points that changed?
    # Can only manage ~3k pixels with draw rects for the cost of blit_arr(1920*1080)
    # Pixelarray would just be even slower than blit_array? Only if every single pixel is changed?
    active_layer = c_frame % 2
    disp_arr = (c_board[active_layer, :, :], c_board[active_layer, 1:-1, 1:-1])[TOROIDAL_ENV]
    pygame.surfarray.blit_array(screen, disp_arr if SCALE == 1 else
                                np.repeat(np.repeat(disp_arr, SCALE, axis=0), SCALE, axis=1))
    pygame.display.update()


def blit_func():
    pygame.surfarray.blit_array(screen, c_board[0, 1:-1, 1:-1])


def write_func():
    screen_raw_buffer.write(np.ascontiguousarray(c_board[0, 1:-1, 1:-1]))


def profile_function(function, n_trials=3, n_per_trial=10):
    global count_over_2ms
    times = timeit.repeat(setup="from __main__ import " + function, stmt=function+"()",
                          repeat=n_trials, number=n_per_trial)
    runtime_ms = 1000 * (min(times) / n_per_trial)
    count_over_2ms += 1 if runtime_ms > 2 else 0
    print("Frame {:3d} : {:12s} ~{:.2f}ms : {:.0f}% Over 2ms".format(c_frame, function + "()", runtime_ms, 100 * count_over_2ms / c_frame))


def empty_region_print(max_window_w):
    print("Empty NxN Ratios:")
    active_layer = c_frame % 2
    wide_count = c_board[active_layer, 1:-1, 1:-1].copy()
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
    global c_frame
    # pygame.surfarray.blit_array(screen, np_board[1:-1, 1:-1])
    # pygame.surfarray.blit_array(screen, c_board[flag, 1:-1, 1:-1])
    # pygame.display.update()
    # step_toroidal_moore_np()
    cy.iterate_multithread(c_board, flag)
    status_print(c_frame) if c_frame % (required_frames // num_reports) == 0 else None
    c_frame += 1


screen_raw_buffer = screen.get_buffer()
c_frame = 1
required_frames = 1000
num_reports = 20

time_init_end = time.time()
print("Total Initialization.... {:.0f}ms".format(1000 * (time_init_end - time_init_start)))
print("\nCore-loop clock starting...", flush=True)
time_chunk_start = time.time()
time_start = time.time()

# cy.iterate_pure_singlethread_sepconv(c_board)
# cy.iterate_pure(c_board, required_frames)
# time_end = time.time()
# print("Avg. {:.2f}FPS".format(required_frames / (time_end - time_start)))
# c_frame += required_frames

done = False
while not done and not c_frame > required_frames:
# while not done:
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
        # generate_frame() if event.type == pygame.MOUSEBUTTONDOWN else None
    generate_frame()
    clock.tick()

c_frame -= 1
time_end = time.time()
print("Core-loop clock stopped...\n", flush=True)
print("Runtime {:.0f}s".format(time_end - time_start))
print("#Frames ", c_frame)
print("Avg. {:.2f}ms Frametime".format(1000 * (time_end - time_start) / c_frame))
print("Avg. {:.2f}FPS".format(c_frame / (time_end - time_start)))
print("\nExiting...")
