import numpy as np
from copy import deepcopy


class ValueIteration:

    '''
    Definition
    __________

    Class to perform Value Iteration


    Class Attributes
    ________________

    discount_factor : float
        Factor with which future rewards are to be discounted

    analysis_data : dict
        Data stored during value iteration for future analysis


    Methods
    _______

    get_analysis_data() : Returns the data captured for analysis

    solve_mdp(mdp, error) : Solves the Markov Decision Process

    get_optimal_policy(mdp, utilities) : Returns the greedy optimal policy based on utilites calculated

    '''

    def __init__(self, discount_factor=0.99):
        '''
        Definition
        __________

        Initializes the ValueIteration class


        Parameters
        __________

        discount_factor : float
            Factor with which future rewards are to be discounted

        '''

        self.discount_factor = discount_factor
        self.analysis_data = {}

    def get_analysis_data(self):
        '''
        Definition
        __________

        Returns the data across iterations stored for analysis 

        '''

        return self.analysis_data

    def solve_mdp(self, mdp, error):
        '''
        Definition
        __________

        Solves the Markov Decision Process using Value Iteration


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc

        error : float
            The maximum acceptable error in utility value for each cell

        '''

        # initialize the utility of each cell as 0 before the value iteration
        utilities = [[0 for i in range(mdp.get_grid_width())]
                     for j in range(mdp.get_grid_height())]

        # calculate change threshold for terminating value iteration loop
        threshold = error * (1 - self.discount_factor) / self.discount_factor

        # initilize analysis data for each cell
        for row in range(mdp.get_grid_height()):
            for col in range(mdp.get_grid_width()):
                analysis_data_key = "(" + str(col) + "," + str(row) + ")"
                self.analysis_data[analysis_data_key] = [0]

        # iterate while terminating condition is not met
        num_iters = 0
        while True:
            num_iters += 1
            max_utility_change = float("-inf")

            # create a deecopy of utilities to make changes on
            updated_utilities = deepcopy(utilities)

            for row in range(mdp.get_grid_height()):
                for col in range(mdp.get_grid_width()):

                    # key for the analysis_data dictionary
                    analysis_data_key = "(" + str(col) + "," + str(row) + ")"

                    # if current cell is a wall, update analysis data with 0 change in utility
                    if mdp.is_wall(row, col):
                        self.analysis_data[analysis_data_key].append(0)
                    else:

                        # initialize utility for the optimal action
                        optimal_action_utility = float("-inf")

                        # iterate through each possible action
                        for action in mdp.get_actions():
                            curr_action_utility = 0

                            # retrieve the transition model: P(s'|s, a)
                            transition_model = mdp.get_transition_model(
                                row, col, action)

                            # iterate through each new state in the transition model
                            # the robot can be in a state different than the intended one due to the nature of the transition model
                            for new_state in transition_model:
                                transition_probability = transition_model[new_state]
                                transition_utility = utilities[new_state[0]
                                                               ][new_state[1]]

                                # add the utility of transition multiplied by the probability of that transition happening
                                curr_action_utility += transition_probability * transition_utility

                            # optimal action is the one with the maximum utility
                            optimal_action_utility = max(
                                optimal_action_utility, curr_action_utility)

                        # collect reward for transition
                        reward = mdp.get_reward(row, col)

                        # record the updated utility
                        updated_utilities[row][col] = reward + \
                            self.discount_factor * optimal_action_utility

                        # record change in utility as a result of the step
                        max_utility_change = max(
                            max_utility_change, abs(updated_utilities[row][col] - utilities[row][col]))

                        # record update utility for data analysis
                        self.analysis_data[analysis_data_key].append(
                            updated_utilities[row][col])

            # update the utility values after each iteration
            utilities = deepcopy(updated_utilities)

            # if the change in utility across all cells is smaller than the change threshold, exit the loop
            if max_utility_change < threshold:
                break

        # get the optimal policy based on final utility values
        optimal_policy = self.get_optimal_policy(mdp, utilities)

        # return the information to the caller
        return {
            "num_iters": num_iters,
            "utilities": utilities,
            "optimal_policy": optimal_policy
        }

    def get_optimal_policy(self, mdp, utilities):
        '''
        Definition
        __________

        Returns the greedy optimal policy based on the utility values calculated by solve_mdp()


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc

        utilities : two-dimensional list
            The utility value of each cell in the grid

        '''

        # initialize the policy to go down at all cells
        policy = [[(1, 0) for col in range(mdp.get_grid_width())]
                  for row in range(mdp.get_grid_height())]

        # iterate over all cells to determine policy
        for row in range(mdp.get_grid_height()):
            for col in range(mdp.get_grid_width()):

                # if the current cell is not a wall, only then process it
                if not mdp.is_wall(row, col):

                    # initialize optimal action and corresponding optimal utility
                    optimal_action = None
                    optimal_action_utility = float("-inf")

                    # iterate over all the actions
                    for curr_action in mdp.get_actions():

                        # initiallize utility of current action to 0
                        curr_action_utility = 0

                        # retrieve the transition model: P(s'|s,a)
                        transition_model = mdp.get_transition_model(
                            row, col, curr_action)

                        # iterate through each new state in the transition model
                        # the robot can be in a state different than the intended one due to the nature of the transition model
                        for new_state in transition_model:
                            transition_probability = transition_model[new_state]
                            transition_utility = utilities[new_state[0]
                                                           ][new_state[1]]

                            # add the utility of transition multiplied by the probability of that transition happening
                            curr_action_utility += transition_probability * transition_utility

                        # if utility of current action is more than the best one so far
                        # then the current action is the optimal action so far
                        if curr_action_utility > optimal_action_utility:
                            optimal_action = curr_action
                            optimal_action_utility = curr_action_utility

                    # record the most optimal action for the current cell
                    policy[row][col] = optimal_action

        # return the optimal policy to the caller
        return policy
