from copy import deepcopy


class PolicyIteration:

    '''
    Definition
    __________

    Class to perform Policy Iteration


    Class Attributes
    ________________

    discount_factor : float
        Factor with which future rewards are to be discounted

    num_policy_eval_iters : int
        Number of iterations for the policy evaluation step

    analysis_data : dict
        Data stored during value iteration for future analysis


    Methods
    _______

    get_analysis_data() : Returns the data captured for analysis

    get_initial_policy() : Returns the initial policy, which defaults to going right at each cell

    solve_mdp(mdp, error) : Solves the Markov Decision Process

    evaluate_policy(mdp, utilities, policy) : Policy evaluation step to evaluate the policy and return the utilites at each cell

    improve_policy(mdp, utilities, policy) : Policy improvement step to find optimal policy based on updated utilities   

    '''

    def __init__(self, discount_factor, num_policy_eval_iters):
        '''
        Definition
        __________

        Initializes the PolicyIteration class


        Parameters
        __________

        discount_factor : float
            Factor with which future rewards are to be discounted

        num_policy_eval_iters : int
            Number of iterations for the policy evaluation step

        '''

        self.discount_factor = discount_factor
        self.num_policy_eval_iters = num_policy_eval_iters
        self.analysis_data = {}

    def get_analysis_data(self):
        '''
        Definition
        __________

        Returns the data across iterations stored for analysis

        '''

        return self.analysis_data

    def get_initial_policy(self, mdp):
        '''
        Definition
        __________

        Returns the initial policy, which defaults to going right at each cell


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc
        '''

        random_start_policy = [[(0, 1) for col in range(
            mdp.get_grid_width())] for row in range(mdp.get_grid_height())]
        return random_start_policy

    def solve_mdp(self, mdp):
        '''
        Definition
        __________

        Solves the Markov Decision Process using Policy Iteration


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc

        '''

        # initialize the initial policy for each cell
        policy = self.get_initial_policy(mdp)

        # initialize the utility of each cell as 0 before the value iteration
        utilities = [[0 for col in range(mdp.get_grid_width())]
                     for row in range(mdp.get_grid_height())]

        # initilize analysis data for each cell
        for row in range(mdp.get_grid_height()):
            for col in range(mdp.get_grid_width()):
                analysis_data_key = "(" + str(col) + "," + str(row) + ")"
                self.analysis_data[analysis_data_key] = [0]

        num_iters = 0

        # use a variable to record whether policy has changed in the policy improvement step
        policy_unchanged = False

        # iterate while the policy is still changing at each improvement step
        while not policy_unchanged:

            # evaluate policy to get utilies at each cell
            utilities = self.evaluate_policy(mdp, utilities, policy)
            num_iters += self.num_policy_eval_iters

            # improve policy based on the updated utilities, to get the final optimal policy
            policy, policy_unchanged = self.improve_policy(mdp,
                                                           utilities, policy)

        # Return the required information to the caller
        return {
            "num_iters": num_iters,
            "utilities": utilities,
            "optimal_policy": policy
        }

    def evaluate_policy(self, mdp, utilities, policy):
        '''
        Definition
        __________

        Policy evaluation step to evaluate the policy and return the utilites at each cell


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc

        utilities : two-dimensional list
            The utility value of each cell in the grid

        policy : two-dimensional list
            The existing action to be taken at each cell

        '''

        # carry out policy evaluation for a specific number of steps
        for i in range(self.num_policy_eval_iters):

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

                        # initialize the current action and set its utility to 0
                        curr_action = policy[row][col]
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

                        # collect reward for transition
                        reward = mdp.get_reward(row, col)

                        # record the updated utility
                        updated_utilities[row][col] = reward + \
                            self.discount_factor * curr_action_utility

                        # record update utility for data analysis
                        self.analysis_data[analysis_data_key].append(
                            updated_utilities[row][col])

            # update the utility values after each iteration
            utilities = deepcopy(updated_utilities)

        # return the utilities of each cell after evaluation is done
        return utilities

    def improve_policy(self, mdp, utilities, policy):
        '''
        Definition
        __________

        Policy improvement step to find optimal policy based on updated utilities


        Parameters
        __________

        mdp : Environment
            The environment of the Markov Decision Process to solve, which specifies the transition model etc

        utilities : two-dimensional list
            The utility value of each cell in the grid

        policy : two-dimensional list
            The existing action to be taken at each cell

        '''

        # create a deepcopy of the current policy to make changes on
        improved_policy = deepcopy(policy)

        # iterate over all cells to determine policy
        for row in range(mdp.get_grid_height()):
            for col in range(mdp.get_grid_width()):

                # if the current cell is not a wall, process it
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
                    improved_policy[row][col] = optimal_action

        # return the improved policy to the caller, with a flag to indicate whether it has changed or not
        return improved_policy, improved_policy == policy
