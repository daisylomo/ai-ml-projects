import pygame
pygame.init()

# value iteration settings
val_iter_discount_factor = 0.99
val_iter_scaler = 0.05
MAX_REWARD = 1
val_iter_error = val_iter_scaler * MAX_REWARD

# policy iteration settings
policy_iter_discount_factor = 0.99
policy_iter_num_policy_eval_iters = 100

# grid settings
grid_width = 6
grid_height = 6
grid = [
    ['G', 'wall', 'G', '', '', 'G'],
    ['', 'B', '', 'G', 'wall', 'B'],
    ['', '', 'B', '', 'G', ''],
    ['', '', '', 'B', '', 'G'],
    ['', 'wall', 'wall', 'wall', 'B', ''],
    ['', '', '', '', '', ''],
]

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
cell_size = 80
height = 480
width = 480

UTILITY_FONT_SIZE = 15
UTILITY_CELL_OFFSET = (20, 25)
POLICY_FONT_SIZE = 30
POLICY_CELL_OFFSET = (30, 15)
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
