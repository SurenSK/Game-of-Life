import pygame
import random
import math
import time
import numpy as np
from scipy import signal
from scipy import ndimage

BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

BOARD_W, BOARD_H = 1920, 1080
OFF_COLOR = WHITE
ON_COLOR = BLACK

pygame.init()
screen = pygame.display.set_mode((BOARD_W, BOARD_H), depth=8)
pygame.display.set_palette([OFF_COLOR]+[ON_COLOR])
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

board_numpy = np.random.choice(a=[0, 1], size=(BOARD_W, BOARD_H))
kernel_h = np.array([1, 1, 1])


# ~45ms at 1920x1080 w/ 1x1 cells
def numpy_toroidal_moore():
    # global n_neighbors, board_numpy
    n_neighbors = ndimage.convolve1d(ndimage.convolve1d(board_numpy, kernel_h, axis=0, mode="wrap"), kernel_h, axis=1, mode="wrap") - board_numpy
    board_numpy[n_neighbors != 2] = 0
    board_numpy[n_neighbors == 3] = 1


# ~7ms at 1920x1080 w/ 1x1 cells
def draw_board():
    pygame.surfarray.blit_array(screen, board_numpy)
    pygame.display.flip()


def status_print(c_frame_n: int, frequency: int) -> None:
    if c_frame_n % frequency == 0:
        print("{:.1f}ms Avg.Frametime over {:4d} Frames\t\tRuntime: {:6.3f}s"
              .format((1000 * (time.time() - time_start) / c_frame_n), c_frame_n, (time.time() - time_start)))


# ~2.5ms overhead
frame_n = 0
required_frames = 10000
print("\nStarting clock...")
time_start = time.time()
done = False
while not done:
    frame_n += 1
    done = frame_n > required_frames
    for event in pygame.event.get():
        done = True if event.type == pygame.QUIT else False
    numpy_toroidal_moore()
    draw_board()
    status_print(frame_n, 100)
    clock.tick()

time_end = time.time()
print("Stopped clock...\n")
print("RunTime ", (time_end - time_start))
print("#Frames ", frame_n)
print("ms per frame ", 1000 * (time_end - time_start) / frame_n)
print("\nExiting...")
