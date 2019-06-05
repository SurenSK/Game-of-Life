import pygame
import random
import math
from typing import List

BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
GRID_COLOR = GRAY
OFF_COLOR = WHITE
ON_COLOR = BLACK
BOARD_WIDTH, BOARD_HEIGHT = 961, 961
CELL_WIDTH, CELL_HEIGHT = 5, 5
BUFFER_SIZE = 1
N_X = math.floor((BOARD_WIDTH-BUFFER_SIZE)/(CELL_WIDTH+BUFFER_SIZE))
N_Y = math.floor((BOARD_HEIGHT-BUFFER_SIZE)/(CELL_HEIGHT+BUFFER_SIZE))
TOT_CELL_W = BUFFER_SIZE + CELL_WIDTH
TOT_CELL_H = BUFFER_SIZE + CELL_HEIGHT

pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
clock = pygame.time.Clock()

n_board = [[random.randint(0, 1) == 1 for x in range(N_X)] for y in range(N_Y)]


# ~0ms to concatenate & print once for 961x961 board w/ 5x5 cell w/ 1 buffer
# ~66ms to print each character separately for 961x961 board w/ 5x5 cell w/ 1 buffer
def board_print(_board: list) -> None:
    board_state = ""
    for x in range(N_X):
        for y in range(N_Y):
            board_state += str(_board[x][y]==1,", ")
            # print(_board[x][y], sep='', end='')
        board_state += "\r\n"
        # print("")
    board_state += "-" * N_X
    # print("-" * N_X)
    print(board_state)


# Just cuts off at board edges
def simulate_flat_moore(old_board: list) -> list:
    new_board = [[0 for x in range(N_X)] for y in range(N_Y)]
    for x in range(N_X):
        for y in range(N_Y):
            neighbors = []
            [[neighbors.append(old_board[xx][yy]) if (not(xx == x and yy == y)) else None
              for xx in range(max(x-1, 0), min(x+2, N_X))]
             for yy in range(max(y-1, 0), min(y+2, N_Y))]
            n_neighbors = sum(neighbors) * (1, -1)[old_board[x][y] == 0]
            new_board[x][y] = 1 if n_neighbors == -3 or n_neighbors == 2 or n_neighbors == 3 else 0
    return new_board


# Wrap-around / Toriodal Topography
# ~2ms for 961x961 board w/ 5x5 cell w/ 1 buffer
def simulate_toroidal_moore(old_board: list) -> list:
    new_board = [[False for x in range(N_X)] for y in range(N_Y)]
    for x in range(N_X):
        col_x = BUFFER_SIZE + (TOT_CELL_W * x)
        neg_x = x - 1
        pos_x = (x + 1) % N_X
        for y in range(N_Y):
            pos_y = (y + 1) % N_Y
            neg_y = y - 1
            n_neighbors = old_board[x][neg_y] + old_board[x][pos_y] + \
                old_board[neg_x][neg_y] + old_board[neg_x][y] + old_board[neg_x][pos_y] + \
                old_board[pos_x][neg_y] + old_board[pos_x][y] + old_board[pos_x][pos_y]

            if n_neighbors > 3:
                continue
            elif n_neighbors < 2:
                continue
            elif n_neighbors == 3:
                new_board[x][y] = True
                if old_board[x][y] is False:
                    pygame.draw.rect(screen, ON_COLOR, [col_x, BUFFER_SIZE + (TOT_CELL_H * y), CELL_WIDTH, CELL_HEIGHT])
            elif old_board[x][y] is True:
                new_board[x][y] = True
                pygame.draw.rect(screen, ON_COLOR, [col_x, BUFFER_SIZE + (TOT_CELL_H * y), CELL_WIDTH, CELL_HEIGHT])
    return new_board


done = False
avg_fps = 0
i = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(OFF_COLOR)
    n_board = simulate_toroidal_moore(n_board)
    pygame.display.flip()
    avg_fps += clock.get_fps()
    i += 1
    done = i == 1000
    print(clock.get_fps())
    clock.tick()

print("Avg FPS", avg_fps/i)
print("Exiting...")
