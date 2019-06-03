import pygame
import random
import math

BLACK, GRAY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
GRID_COLOR = GRAY
OFF_COLOR = WHITE
ON_COLOR = BLACK
BOARD_WIDTH, BOARD_HEIGHT = 951, 951
CELL_WIDTH, CELL_HEIGHT = 5, 5
BUFFER_SIZE = 1
N_X = math.floor((BOARD_WIDTH-BUFFER_SIZE)/(CELL_WIDTH+BUFFER_SIZE))
N_Y = math.floor((BOARD_HEIGHT-BUFFER_SIZE)/(CELL_HEIGHT+BUFFER_SIZE))


# Just cuts off at board edges
def calc_new_board(old_board: list) -> list:
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


def board_print(_board: list) -> None:
    for x in range(N_X):
        for y in range(N_Y):
            print(_board[x][y], sep='', end='')
        print("")
    print("-" * N_X)


pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
clock = pygame.time.Clock()

board = [[random.randint(0, 1) for x in range(N_X)] for y in range(N_Y)]
# board = [[0 for x in range(N_X)] for y in range(N_Y)]

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
#        if event.type == pygame.KEYDOWN:
#            board = calc_new_board(board)
#            board_print(board)

    screen.fill(GRID_COLOR)
#    board_print(board)
    for x in range(N_X):
        for y in range(N_Y):
            pygame.draw.rect(screen, (ON_COLOR, OFF_COLOR)[board[y][x] == 0],
                             [BUFFER_SIZE + (BUFFER_SIZE + CELL_WIDTH) * x,
                              BUFFER_SIZE + (BUFFER_SIZE + CELL_HEIGHT) * y,
                              CELL_WIDTH, CELL_HEIGHT])
    pygame.display.flip()
    board = calc_new_board(board)
    clock.tick(12)

print("Exiting...")
