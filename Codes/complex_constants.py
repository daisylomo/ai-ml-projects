import numpy as np
from random import uniform
import pygame
pygame.init()

# value iteration settings
val_iter_discount_factor = 0.99
val_iter_scaler = 0.1
MAX_REWARD = 1
val_iter_error = val_iter_scaler * MAX_REWARD

# policy iteration settings
policy_iter_discount_factor = 0.99
policy_iter_num_policy_eval_iters = 100

# grid settings
np.random.seed(42)
grid_width = 18
grid_height = 18
grid = []

for row in range(grid_height):
    grid_row = []
    for col in range(grid_height):
        random_num = uniform(0, 1)
        if random_num <= 0.25:
            grid_row.append("wall")
        elif random_num <= 0.4:
            grid_row.append("G")
        elif random_num <= 0.55:
            grid_row.append("B")
        else:
            grid_row.append("")
    grid.append(grid_row)

actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

reward_mapping = {
    'wall': 0,
    'G': 1,
    'B': -1,
    '': -0.04
}
rewards = [[reward_mapping[grid[row][col]]
            for col in range(grid_width)] for row in range(grid_height)]

# mapping for action to arrow symbol
ACTION_TUPLE_CONVERSION = {(1, 0): '⬇', (-1, 0): '⬆',
                           (0, 1): '➡', (0, -1): '⬅'}

# display settings
cell_size = 50
height = 900
width = 900

UTILITY_FONT_SIZE = 15
UTILITY_CELL_OFFSET = (7, 14)
POLICY_FONT_SIZE = 20
POLICY_CELL_OFFSET = (18, 10)
POLICY_FONT = pygame.font.Font(
    "seguisym.ttf", int(POLICY_FONT_SIZE))
UTILITY_FONT = pygame.font.Font(
    "seguisym.ttf", int(UTILITY_FONT_SIZE))

# user interface settings
SCREEN_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
GREEN = (0, 255, 0)
BROWN = (255, 140, 0)
