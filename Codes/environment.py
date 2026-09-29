from collections import defaultdict


class Environment:

    '''
    Definition
    __________

    Class to setup the Markov Decision Process Environment


    Class Attributes
    ________________

    grid : two-dimensional list
        The grid world

    height : int
        Height of the grid

    width : int
        Width of the grid

    actions : list
        A list of possible actions - UP, DOWN, LEFT, RIGHT

    rewards : two-dimensional list
        The reward at each cell in the grid


    Methods
    _______

    get_reward(row, col) : Returns the reward for a particular cell in the grid

    get_actions() : Returns the list of possible actions that can be taken

    get_grid_height() : Returns the height of the grid

    get_grid_width() : Returns the width of the grid

    get_transition_model(row, col, action) : Returns the transition model P(s'|s,a) for a particular state and action

    is_wall(row, col) : Returns whether the specified cell is a wall or not

    '''

    def __init__(self, grid, height, width, actions, rewards):
        '''
        Definition
        __________

        Initializes the Environment class


        Parameters
        __________

        grid : two-dimensional list
            The grid world

        height : int
            Height of the grid

        width : int
            Width of the grid

        actions : list
            A list of possible actions - UP, DOWN, LEFT, RIGHT

        rewards : two-dimensional list
            The reward at each cell in the grid

        '''

        self.grid = grid
        self.height = height
        self.width = width
        self.actions = actions
        self.rewards = rewards

    def get_reward(self, row, col):
        '''
        Definition
        __________

        Returns the reward for a particular cell in the grid


        Parameters
        __________

        row : int
            The row (indexed from 0) of the specified state

        col : int
            The column (indexed from 0) of the specified state

        '''

        return self.rewards[row][col]

    def get_actions(self):
        '''
        Definition
        __________

        Returns the list of possible actions that can be taken

        '''

        return self.actions

    def get_grid_height(self):
        '''
        Definition
        __________

        Returns the height of the grid 

        '''

        return self.height

    def get_grid_width(self):
        '''
        Definition
        __________

        Returns the width of the grid 

        '''

        return self.width

    def get_transition_model(self, row, col, action):
        '''
        Definition
        __________

        Returns the transition model P(s'|s,a) for a particular state and action


        Parameters
        __________

        row : int
            The row (indexed from 0) of the specified state

        col : int
            The column (indexed from 0) of the specified state

        action: tuple
            The action that is being taken

        '''

        # initialize the transition model as a dictionary to store the mappings
        transition_model = defaultdict(int)

        # dir_and_probability lists the probability of a particular direction of movement
        # as well as the offset to be added to the current coordinates to retrieve the
        # updated coordinates
        dir_and_probability = [
            [0.8, action],
            [0.1, (-action[1], -action[0])],
            [0.1, (action[1], action[0])]
        ]

        # iterate over all the possible directions of movement
        for probability, direction in dir_and_probability:
            new_row = row + direction[0]
            new_col = col + direction[1]

            # process further only if the new coordinates are valid coordinates
            if 0 <= new_row < self.get_grid_height() and 0 <= new_col < self.get_grid_width():

                # if the new coordinates are that of a wall, then the agent stays in the current state
                if self.grid[new_row][new_col] == "wall":
                    new_row, new_col = row, col

            # otherwise the agent remains in the current state
            else:
                new_row, new_col = row, col

            # add the probability to the updated state entry in the transition model
            transition_model[(new_row, new_col)] += probability

        # return the transition model to the caller
        return transition_model

    def is_wall(self, row, col):
        '''
        Definition
        __________

        Returns whether the specified cell is a wall or not


        Parameters
        __________

        row : int
            The row (indexed from 0) of the specified state

        col : int
            The column (indexed from 0) of the specified state

        '''

        return self.grid[row][col] == "wall"
