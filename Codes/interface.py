from constants import *
import pygame
pygame.init()


class Interface(object):

    '''
    Definition
    __________

    Class to define the User Interface for displaying policy and utilities of each cell, using PyGame


    Class Attributes
    ________________

    cell_size : int
        Size for each cell in the grid

    height : int
        Height of the grid

    width : int
        Width of the grid


    Methods
    _______

    get_grid_colors(grid) : Returns the color of each cell, as a two-dimensional array

    solve_mdp(mdp, error) : Solves the Markov Decision Process

    display(arr, grid, offset, font, title='Grid World') : Starts the PyGame display window, with the specified settings

    '''

    def __init__(self, cell_size=80, height=480, width=480):
        '''
        Definition
        __________

        Initializes the Interface class


        Parameters
        __________

        cell_size : int
            Size for each cell in the grid

        height : int
            Height of the grid

        width : int
            Width of the grid

        '''

        # initialize the super class
        super().__init__()
        self.cell_size = cell_size
        self.height = height
        self.width = width
        self.screen_dims = (height, width)

    def get_grid_colors(self, grid):
        '''
        Definition
        __________

        Returns the color of each cell, as a two-dimensional array


        Parameters
        __________

        grid : two-dimensional list
            The grid, with each cell having one of the following values: 'G' / 'B' / 'wall' / ''

        '''

        colors = []

        # iterate over each cell of the grid
        for row in grid:
            color = []
            for cell in row:

                # add the color depending on the cell content
                if cell == 'G':
                    color.append(GREEN)
                elif cell == 'B':
                    color.append(BROWN)
                elif cell == 'wall':
                    color.append(GREY)
                else:
                    color.append(WHITE)
            colors.append(color)

        # return the two-dimensional list of colors for each cell
        return colors

    def display(self, arr, grid, offset, font, title="Grid World"):
        '''
        Definition
        __________

        Starts the PyGame display window, with the specified settings


        Parameters
        __________

        arr : two-dimensional list
            Contains the content of each cell to be displayed

        grid : two-dimensional list
            Contains the actual grid of the Markov Dimension Process

        offset : tuple of ints
            Offset of the cell content from the cell border

        font : pygame.font.Font
            The font style for the content of the cell

        title : string
            Title of the PyGame display window

        '''

        # open the pygame screen display
        screen = pygame.display.set_mode(self.screen_dims)
        pygame.display.set_caption(title)

        # set the grid colors using helper function get_grid_colors()
        colors = self.get_grid_colors(grid)

        # initialize a flag to indicate whether display window should stop or continue
        stop_flag = False

        # iterate while pygame display window is not quit
        while not stop_flag:

            # register current event
            for event in pygame.event.get():

                # if current event is quit, then exit
                if event.type == pygame.QUIT:
                    stop_flag = True

            # draw the display window
            rect = pygame.Rect(0, 0, self.width, self.height)
            pygame.draw.rect(screen, SCREEN_COLOR, rect)

            # iterate through each cell in the grid
            for row in range(len(grid)):
                for col in range(len(grid)):
                    rect = pygame.Rect(
                        col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, colors[row][col], rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                    # if the current cell is not a wall, then process the text to display
                    if grid[row][col] != 'wall':

                        # set the message to be displayed in the current cell
                        message = font.render(
                            arr[row][col], True, (0, 0, 0))

                        # add the message to the current cell for display
                        screen.blit(message, (col * self.cell_size +
                                              offset[0], row * self.cell_size + offset[1]))

            # update the pygame display window
            pygame.display.update()
