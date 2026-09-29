# import the required files to execute the program
from algorithms.value_iteration import ValueIteration
from algorithms.policy_iteration import PolicyIteration
from data_recorder import DataRecorder
from environment import Environment
from interface import Interface

from constants import *
# uncomment below line and comment the above line to use custom grid
# from complex_constants import *

# initialize variables used for both value iteration and policy iteration
interface = Interface(cell_size, height, width)
mdp = Environment(grid, grid_height, grid_width, actions, rewards)
data_recorder = DataRecorder("recorded_data/")

# display the menu until the correct option is chosen
while True:
    print("Choose algorithm")
    print("1. Value Iteration")
    print("2. Policy Iteration")
    print("3. Exit")
    choice = int(input())
    print()

    # if the user has chosen the run value iteration
    if choice == 1:
        value_iteration = ValueIteration(val_iter_discount_factor)
        result = value_iteration.solve_mdp(mdp, val_iter_error)

        num_iters = result["num_iters"]
        utilities = result["utilities"]
        optimal_policy = result["optimal_policy"]

        print("Number of iterations = " + str(num_iters))
        print()
        print("Cell-wise utilities: (Col, Row)")
        print()
        # display the utilities of each cell, formatted as (col, row), in the command line
        for row in range(grid_height):
            for col in range(grid_width):
                print("(" + str(col) + "," + str(row) + "): " +
                      str(utilities[row][col]))
        print()

        # display policy on the pygame interface
        direction_array = [[ACTION_TUPLE_CONVERSION[optimal_policy[row][col]]
                            for col in range(grid_width)] for row in range(grid_height)]
        interface.display(arr=direction_array, grid=grid, offset=POLICY_CELL_OFFSET,
                          font=POLICY_FONT, title='Value Iteration Policy')

        # display utilities on the pygame interface
        utility_values = [["{:.2f}".format(utilities[row][col]) for col in range(
            grid_width)] for row in range(grid_height)]
        interface.display(arr=utility_values, grid=grid, offset=UTILITY_CELL_OFFSET,
                          font=UTILITY_FONT, title='Value Iteration Utilities')

        # record data of algorithm execution into a csv, for future data analysis
        data_recorder.record("value_iteration.csv",
                             value_iteration.get_analysis_data())

        break

    # if the user has chosen the run policy iteration
    elif choice == 2:
        policy_iteration = PolicyIteration(
            policy_iter_discount_factor, policy_iter_num_policy_eval_iters)
        result = policy_iteration.solve_mdp(mdp)

        num_iters = result["num_iters"]
        utilities = result["utilities"]
        optimal_policy = result["optimal_policy"]

        print("Number of iterations = " + str(num_iters))
        print()
        print("Cell-wise utilities: (Col, Row)")
        print()
        for row in range(grid_height):
            for col in range(grid_width):
                print("(" + str(col) + "," + str(row) + "): " +
                      str(utilities[row][col]))
        print()

        # display policy on the pygame interface
        direction_array = [[ACTION_TUPLE_CONVERSION[optimal_policy[row][col]]
                            for col in range(grid_width)] for row in range(grid_height)]
        interface.display(arr=direction_array, grid=grid, offset=POLICY_CELL_OFFSET,
                          font=POLICY_FONT, title='Policy Iteration Policy')

        # display utilities on the pygame interface
        utility_values = [["{:.2f}".format(utilities[row][col]) for col in range(
            grid_width)] for row in range(grid_height)]
        interface.display(arr=utility_values, grid=grid, offset=UTILITY_CELL_OFFSET,
                          font=UTILITY_FONT, title='Policy Iteration Utilities')

        # record data of algorithm execution into a csv, for future data analysis
        data_recorder.record("policy_iteration.csv",
                             policy_iteration.get_analysis_data())

        break

    # if the user has chosen the exit the program
    elif choice == 3:
        print("Exiting...")
        break

    # if the user enters a number not available in the menu
    else:
        print("Incorrect choice. Please enter choice again!")
        print()
