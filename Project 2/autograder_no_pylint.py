""" Simple autograder for EP2 USP AI Course """
import os
import sys
#import concurrent.futures
import signal
#import time
import util

try:
    import ep2
    from ep2 import *
except Exception as e:
    if os.path.exists("final_result.txt"):
        file_flag = "a"
    else:
        file_flag = "w"

    file_results = open("final_result.txt", file_flag)
    file_results.write("******************************\n")
    file_results.write("Your code does not even import!\n")
    file_results.write("------------------------------\n")
    file_results.write("Unable to perform any check or test\n")
    file_results.write("Grades are:\nTest00: 0.0\nTest01: 0.0\n")
    file_results.write("Test02: 0.0\n")
    file_results.close()
    sys.exit(1)


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        """ Extends the Exception class """
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


def run_tests():
    """ Simple function to perform a small subset of tests for EP2 """
    if os.path.exists("final_result.txt"):
        file_flag = "a"
    else:
        file_flag = "w"
    file_results = open("final_result.txt", file_flag)
    final_grades = []  # Grade list (code, p01_01, p01_02, p02, p03)
    lint_score = -1000
    final_grades.append(lint_score)

    #global_results = 0  # Student's result in all tests for all parts
    #total_tests_global = 0  # Number of tests performed in all parts
    #total_tests = 0  # Number of tests in a specific part
    test_results = 0  # Student's result in that specific
    #part_tests = 0  # Keep total tests in each part for weighted score
    #part_correct = 0  # Keep correct in each part for weighted score

    try:
        print("*************************")
        print("Starting tests:")
        print("Starting Part 00: Test 01")
        file_results.write("------------------------------\n")
        file_results.write("Part00: RandomAgent Improved\n")

        # Part00 - 5 tests
        # Default grid: [[1,3,0,3],[7,5,4,2],[3,0,6,0]] Check if no faults
        # Blocking grid [[1,5,3],[2,4,5],[3,0,0]]
        # Blocked and gas [[5,0,5],[5,8,5],[3,9,5]]
        # Big grid 2000x2000 car 1 at (1998,1998), person (1,1), car2 (0,0)
        # Changes in perception

        # Test 01
        # Default grid: [[1,3,0,3],[7,5,4,2],[3,0,6,0]] Check if no faults
        grid1 = [[1, 3, 0, 3], [7, 5, 4, 2], [3, 0, 6, 0]]
        problem = util.USPber(grid=grid1,
                              multi_agent=True,
                              tank_capacity=5,
                              max_turns=20)
        pl1 = ep2.RandomAgent(player_number=1, number_of_agents=2,
                              tank_capacity=5, max_depth=4)
        moves = 0
        is_goal = False
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)

        while moves < 15 and not is_goal:
            with Timeout(10):
                act = pl1.get_action(state1)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            if problem.is_goal_state(new_state):
                final_info = problem.get_game_info(new_state)
                is_goal = True
            else:
                n_grid, _, nt01g, _, _, _ = new_state
                state1 = (n_grid, nt01g)
                final_info = problem.get_game_info(new_state)
                state = copy.deepcopy(new_state)
                moves += 1

        if final_info['agent1_faults'] == 0:
            test_results += 1


        print("Finished Part 00: Test 01")
        print("*************************")
        print("Starting Part 00: Test 02")

        # Test 02
        # Blocking grid [[1,5,3],[2,4,5],[3,0,0]]
        grid2 = [[1, 5, 3], [2, 4, 5], [3, 0, 0]]
        problem = util.USPber(grid=grid2,
                              multi_agent=True,
                              tank_capacity=10,
                              max_turns=20)
        pl1 = ep2.RandomAgent(player_number=1, number_of_agents=2,
                              tank_capacity=10, max_depth=4)
        moves = 0
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)

        while moves < 15:
            with Timeout(10):
                act = pl1.get_action(state1)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            n_grid, _, nt01g, _, _, _ = new_state
            state1 = (n_grid, nt01g)
            final_info = problem.get_game_info(new_state)
            state = copy.deepcopy(new_state)
            moves += 1

        if final_info['agent1_faults'] == 0:
            test_results += 1


        print("Finished Part 00: Test 02")
        print("*************************")
        print("Starting Part 00: Test 03")


        # Test 03
        # Blocked gas [[5,0,5],[5,8,5],[3,9,5]]
        grid3 = [[5, 0, 5], [5, 8, 5], [3, 9, 5]]
        problem = util.USPber(grid=grid3,
                              multi_agent=True,
                              tank_capacity=10,
                              max_turns=201)
        pl1 = ep2.RandomAgent(player_number=1, number_of_agents=2,
                              tank_capacity=10, max_depth=4)
        moves = 0
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)
        list_of_actions = []

        while moves < 200:  # To check if list of actions contains all
            with Timeout(10):
                act = pl1.get_action(state1)
            list_of_actions.append(act)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            n_grid, _, nt01g, _, _, _ = new_state
            state1 = (n_grid, nt01g)
            final_info = problem.get_game_info(new_state)
            state = copy.deepcopy(new_state)
            moves += 1

        if final_info['agent1_faults'] == 0:
            for action in ['STOP', 'REFILL', 'UP', 'DOWN']:
                if action in list_of_actions:
                    test_results += 0.25  # Very low chance to skip one action

        print("Finished Part 00: Test 03")
        print("*************************")
        print("Starting Part 00: Test 04")

        # Test 04
        # Big grid 2000x2000 car 1 at (1998,1998), person (1,1), car2 (0,0)
        grid4 = [[0]*2000 for _ in range(2000)]
        grid4[1][1] = 3
        grid4[0][0] = 2
        grid4[1998][1998] = 1
        problem = util.USPber(grid=grid4,
                              multi_agent=True,
                              tank_capacity=100,
                              max_turns=11)
        pl1 = ep2.RandomAgent(player_number=1, number_of_agents=2,
                              tank_capacity=100, max_depth=4)
        moves = 0
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)
        list_of_actions = []

        while moves < 5:
            with Timeout(15):
                act = pl1.get_action(state1)
            list_of_actions.append(act)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            n_grid, _, nt01g, _, _, _ = new_state
            state1 = (n_grid, nt01g)
            final_info = problem.get_game_info(new_state)
            state = copy.deepcopy(new_state)
            moves += 1

        if final_info['agent1_faults'] == 0:
            test_results += 1.0

        print("Finished Part 00: Test 04")
        print("*************************")
        print("Starting Part 00: Test 05")

        # Test 05
        # Changed perception
        grid5 = [[1, 2], [0, 3]]
        pl1 = ep2.RandomAgent(player_number=1, number_of_agents=2,
                              tank_capacity=10, max_depth=4)
        state1 = (grid5, 10)

        with Timeout(10):
            act = pl1.get_action(state1)
        if act in ['STOP', 'DOWN']:
            test_results += 0.25
        state1 = ([[0, 0, 2], [0, 8, 5], [3, 5, 0]], 6)
        with Timeout(10):
            act = pl1.get_action(state1)
        if act in ['STOP', 'UP', 'LEFT', 'REFILL']:
            test_results += 0.25
        state1 = ([[0, 5, 2], [0, 8, 5], [3, 5, 0]], 0)
        with Timeout(10):
            act = pl1.get_action(state1)
        if act in ['STOP', 'REFILL']:
            test_results += 0.25
        state1 = ([[0, 5, 0], [9, 8, 5], [3, 5, 0]], 3)
        with Timeout(10):
            act = 'STOP'
            while act != 'REFILL':  # To see if car chooses refill action
                act = pl1.get_action(state1)
        if act == 'REFILL':
            test_results += 0.25

        if test_results > 0:
            final_grades.append((10.0*test_results)/5)
        else:
            final_grades.append(0.0)
        # End of Part00
        print("Finished Part 00: Test 05")
        print("*************************")
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not concluded in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades.append((10.0*test_results)/5)
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
    finally:
        if len(final_grades) < 2:
            final_grades.append(0.0)
        file_results.write("Grade in the Test00: {0:.1f}/10.0\n".format(final_grades[1]))


    try:
        test_results = 0
        print("*************************")
        print("Starting Part 01: Test 01")

        file_results.write("------------------------------\n")
        file_results.write("Part01:\n")

        # Part01 - 4 tests
        # Default grid: [[1,3,0,3],[7,5,4,2],[3,0,6,0]] fuel spent(fs)= 9
        # Trick straight line [[3,0,1,6,7,3,5,3], [2,0,0,0,0,0,4,0]] fs=11
        # Refill check [[3,0,0,0,3],[0,0,0,0,0],[0,0,8,0,0],[0,2,0,0,0],[3,0,0,0,3]] fs=28
        # Teleporting person

        # Test 01
        # Default grid: [[1,3,0,3],[7,5,4,2],[3,0,6,0]] Check if no faults
        grid1 = [[1, 3, 0, 3], [7, 5, 4, 2], [3, 0, 6, 0]]
        problem = util.USPber(grid=grid1,
                              multi_agent=True,
                              tank_capacity=5,
                              max_turns=20)
        plr1 = ep2.CollectAllAgent(player_number=1, number_of_agents=2,
                                   tank_capacity=5, max_depth=4)
        moves = 0
        is_goal = False
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)

        while moves < 20 and not is_goal:
            with Timeout(15):
                act = plr1.get_action(state1)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            if problem.is_goal_state(new_state):
                final_info = problem.get_game_info(new_state)
                is_goal = True
            else:
                n_grid, _, nt01g, _, _, _ = new_state
                state1 = (n_grid, nt01g)
                final_info = problem.get_game_info(new_state)
                state = copy.deepcopy(new_state)
                moves += 1

        if final_info['agent1_gas_spent'] <= 9:
            if final_info['agent1_people'] == 18:
                test_results += 1

        print("Finished Part 01: Test 01")
        print("*************************")
        print("Starting Part 01: Test 02")

        # Test 02
        # Trick straight line [[3,0,1,6,7,3,5,3], [2,0,0,0,0,0,4,0]] fs=11
        grid2 = [[3, 0, 1, 6, 7, 3, 5, 3], [2, 0, 0, 0, 0, 0, 4, 0]]
        problem = util.USPber(grid=grid2,
                              multi_agent=True,
                              tank_capacity=10,
                              max_turns=20)

        plr1 = ep2.CollectAllAgent(player_number=1, number_of_agents=2,
                                   tank_capacity=10, max_depth=4)

        moves = 0
        is_goal = False
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)

        while moves < 30 and not is_goal:
            with Timeout(15):
                act = plr1.get_action(state1)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            if problem.is_goal_state(new_state):
                final_info = problem.get_game_info(new_state)
                is_goal = True
            else:
                n_grid, _, nt01g, _, _, _ = new_state
                state1 = (n_grid, nt01g)
                final_info = problem.get_game_info(new_state)
                state = copy.deepcopy(new_state)
                moves += 1

        if final_info['agent1_gas_spent'] <= 11:
            if final_info['agent1_people'] == 18:
                test_results += 1

        print("Finished Part 01: Test 02")
        print("*************************")
        print("Starting Part 01: Test 03")

        # Test 03 fs=28
        # Refill check [[3,0,0,0,3],[0,0,0,0,0],[0,0,8,0,0],[0,2,0,0,0],[3,0,0,0,3]]
        grid3 = [[3, 0, 0, 0, 3],
                 [0, 0, 0, 0, 0],
                 [0, 0, 8, 0, 0],
                 [0, 2, 0, 0, 0],
                 [3, 0, 0, 0, 3]]
        problem = util.USPber(grid=grid3,
                              multi_agent=True,
                              tank_capacity=10,
                              max_turns=70)

        plr1 = ep2.CollectAllAgent(player_number=1, number_of_agents=2,
                                   tank_capacity=10, max_depth=4)

        moves = 0
        is_goal = False
        state = problem.initial_state()
        n_grid, _, nt01g, _, _, _ = state
        state1 = (n_grid, nt01g)

        while moves < 60 and not is_goal:
            with Timeout(20):
                act = plr1.get_action(state1)
            new_state = problem.next_state(state, act)
            new_state = problem.next_state(new_state, 'STOP')
            if problem.is_goal_state(new_state):
                final_info = problem.get_game_info(new_state)
                is_goal = True
            else:
                n_grid, _, nt01g, _, _, _ = new_state
                state1 = (n_grid, nt01g)
                final_info = problem.get_game_info(new_state)
                state = copy.deepcopy(new_state)
                moves += 1

        if final_info['agent1_gas_spent'] <= 28:
            if final_info['agent1_people'] == 4:
                test_results += 1

        print("Finished Part 01: Test 03")
        print("*************************")
        print("Starting Part 01: Test 04")

        # Test 04
        # Teleporting with no solution on some instances
        grid4 = [[3, 0, 0, 1, 0, 0],
                 [2, 0, 0, 4, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]

        plr1 = ep2.CollectAllAgent(player_number=1, number_of_agents=2,
                                   tank_capacity=8, max_depth=4)
        moves = 0
        state1 = (grid4, 8)
        list_of_actions = []
        still_correct = True

        if still_correct:
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'LEFT':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[3, 0, 1, 0, 0, 0],
                     [2, 0, 0, 4, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
            state1 = (grid4, 7)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'LEFT':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 1, 0, 0, 0, 0],
                     [2, 0, 0, 4, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 3, 0, 0, 0, 0]]
            state1 = (grid4, 6)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'DOWN':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 0, 0, 0, 0, 0],
                     [2, 1, 0, 4, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 3, 0, 0, 0, 0]]
            state1 = (grid4, 5)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'DOWN':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 0, 0, 0, 0, 0],
                     [2, 0, 0, 4, 0, 0],
                     [0, 1, 0, 0, 0, 3],
                     [0, 0, 0, 0, 0, 0]]
            state1 = (grid4, 4)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'RIGHT':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 0, 0, 0, 0, 0],
                     [2, 0, 0, 4, 0, 0],
                     [0, 0, 1, 0, 0, 3],
                     [0, 0, 0, 0, 0, 0]]
            state1 = (grid4, 3)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'RIGHT':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 0, 0, 0, 0, 3],
                     [2, 0, 0, 4, 0, 0],
                     [0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
            state1 = (grid4, 2)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'UP':
                still_correct = False
            else:
                test_results += 0.1
        if still_correct:
            grid4 = [[0, 0, 0, 0, 0, 3],
                     [2, 0, 0, 8, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]]
            state1 = (grid4, 1)
            with Timeout(10):
                act = plr1.get_action(state1)
            if act != 'REFILL':
                still_correct = False
            else:
                test_results += 0.3

        if test_results > 0:
            final_grades.append((10.0*test_results)/4)
        else:
            final_grades.append(0.0)

        print("Finished Part 01: Test 04")
        print("*************************")
        print("*************************")
        print("This autograder does not test Part02")
        print("Check final_results.txt for info")
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not concluded in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades.append((10.0*test_results)/116.0)
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not concluded\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
    finally:
        if len(final_grades) < 3:
            final_grades.append(0.0)
        file_results.write("Grade in the Test01: {0:.1f}/10.0\n".format(final_grades[2]))
        file_results.write("------------------------------\n")
        file_results.write("Part02:\n")
        file_results.write("This autograder does not test Part02\n")
        file_results.write("because we need two instances of AlphaBetaAgent:\n")
        file_results.write("    -One using evaluation_function\n")
        file_results.write("    -One using my_better_evaluation_function\n")
        file_results.write("In order to test your implementation\n")
        file_results.write("you should run both instances against GetClosest\n")
        file_results.write("using different game grids, like the ones\n")
        file_results.write("presented in interesting_grids.txt.\n")
        file_results.write("The agent using my_better should be able to\n")
        file_results.write("get equal or higher score in most of the examples.")


if __name__ == "__main__":
    FILE_ABSOLUTE_PATH = os.path.abspath(__file__)
    TEST_DIR = os.path.dirname(FILE_ABSOLUTE_PATH)
    run_tests()
