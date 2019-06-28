#!/usr/bin/python3
"""
########################################################################
#          Auxiliary methods used in USP AI course                     #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#
#                                                                      #
# (C) Copyright 2019 Denis Deratani Maua (denis.maua@usp.br)           #
# (C) Copyright 2019 Decio Lauro Soares (deciolauro@gmail.com)         #
# (C) Copyright 2019 Fabio Henrique Tanaka (fhktanaka@gmail.com)       #
# (C) Copyright 2019 Julissa Villanueva Llerena (jgville@ime.usp.br)   #
########################################################################
"""
import sys
import copy
import heapq

# **********************************************************
# **   GLOBAL CONSTANTS YOU CAN/MAY HAVE TO CHANGE        **
# **********************************************************
MAX_TURNS = 30           # Maximum number of turns until game ends
MAX_DEPTH = 4            # For agents that need to prune, maxdepth until eval.
SHOW_INFO = True         # Flag to display full/minimal info on terminal
SHOW_DISPLAY = True      # Flag to display graphical/terminal game execution
TANK_CAPACITY = 5        # Define the tank capacity to all cars
DEFAULT_REFILL = 10      # Controls the maximum amount of combustive per refill

# **********************************************************
# **   GLOBAL CONSTANTS YOU SHOULD NOT CHANGE             **
# **********************************************************
PROFESSOR_BONUS = 10     # Set the bonus for collecting a professor
MONITOR_BONUS = 5        # Set the bonus for collecting a monitor
STUDENT_BONUS = 1        # Set the bonus for collecting a student
INT_INFTY = sys.maxsize  # Global helper to represent integer infinity
CURRENT_TURN = 0         # Debug/autograder only (set starting turn)
GAME_MONEY = False       # Alternative scoring system (Debug/autograder only!)
MONEY_PER_BONUS = 10     # Alternative scoring system (Debug/autograder only!)
MONEY_PER_FUEL = -2      # Alternative scoring system (Debug/autograder only!)
MONEY_PER_FAULT = -20    # Alternative scoring system (Debug/autograder only!)


class Agent(object):
    """ Abstract class for any Agent

    Every Agent you implement must inherit from Agent class and have to
    extend at the get_action method.

    .. warning::
        The code raises a TypeError exception if you try to instantiate
        this class.
    """
    def __init__(self, **kwargs):
        """ Default constructor for the abstract class.

        You can consider that the only attributes that will be passed to your
        agent during the initialization will be packed in the kwargs dictionary.

        Those attributes will be:

        :param player_number: An identifier for your player in the game
        :param number_of_agents: The number of competing agents in the game
        :param max_depth: For the relevant agents, the depth where you perform
            a prune/cutoff
        :param tank_capacity: The tank capacity of the agent
        :type player_number: <class 'int'>
        :type number_of_agents: <class 'int'>
        :type max_depth: <class 'int'>
        :type tank_capacity: <class 'int'>

        .. note::
            For all your agents, its safe to pass the kwargs dictionary
            directly to here, by doing super().__init__(**kwargs).
            Your only concern should be to create the subclass attributes
            that ARE NOT listed above (like initial_state, problem, ...)

        .. seealso::
            To see examples on how to use this abstract class look into the
            ep2.GetClosestPersonOrRefillAgent or ep2.AlphaBetaAgent

        .. warning::
            The code raises a TypeError exception if you try to instantiate
            this class instead of a subclass.
        """
        if type(self) is Agent:
            raise TypeError('You cannot instantiate this abstract class')

        self.player_number = kwargs.get('player_number', 1)
        self.number_of_agents = kwargs.get('number_of_agents', 2)
        self.max_depth = kwargs.get('max_depth', MAX_DEPTH)
        self.tank_capacity = kwargs.get('tank_capacity', INT_INFTY)
        self.problem = None
        self.initial_state = None


    def get_action(self, perception):
        """ Abstract method

        All your agents MUST extend this method.

        :param perception: A perception that the agent receives from the
            environment
        :type perception: Environment dependent
        :return action: An action from all possible actions for that
            environment
        :rtype: <class 'str'>

        .. notes::
            Unless otherwise stated, you can consider that all perceptions
            will came from the USPber environment and, because of that, will
            be a tuple with the grid matrix and the remaining fuel for your
            agent
        """
        raise NotImplementedError



class Node(object):
    """ Class for usage as search node

    We are providing you few search algorithms (informed search, A* and ucs)
    and for some parts in this programming assignment you are required to
    use our implementation. On those cases, you MUST use this class as a
    search node otherwise the search will fail.

    :var state: Keep a state of the problem
    :var cost: Keep the cost from start state up to current state
    :var parent: Pointer to the parent Node or None if no parent.
    :var action: Action taken.

    :Example:

    >>> my_node = Node((1,2,3), 7)
    >>> my_node.state
    (1, 2, 3)
    >>> my_node.cost
    7
    >>> my_node.parent
    >>> my_node.action
    >>> other_node = Node(state=(1,2,4), cost=9, parent=my_node, action='STOP')
    >>> other_node.state
    (1, 2, 4)
    >>> other_node.cost
    9
    >>> other_node.parent
    <Node (1, 2, 3)>
    >>> other_node.action
    'STOP'

    .. note::
        To make it easier, you are free to direct access all attributes from
        this class or implement your own getters and setters, as long as you
        keep the attributes public.

    .. seealso:
        ep2.GetClosestPersonOrRefillPloblem uses our provided A* algorithm.
        You should check that class to see an example of how to use this class.

    .. warning::
        Like the previous programming assignments, do not confuse yourself,
        you can/may use Node in all your searches, but your agent must process
        the solution and return an ACTION.
    """
    def __init__(self, state, cost, parent=None, action=None):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        if self.parent:
            self.height = self.parent.height + 1
        else:
            self.height = 0


    def __repr__(self):
        return "<Node {}>".format(self.state)



class Problem(object):
    """ Abstract class to represent a Search Problem

    All your problems must be a subclass of this class and must extend all
    the abstract methods presented below.

    .. warning::
        This is an Abstract class and will raise a TypeError exception if
        you try to instantiate it instead of a subclass.
    """
    def initial_state(self):
        """ Abstract method to get the initial state """
        raise NotImplementedError
    def actions(self, state):
        """ Abstract method that returns a list of valid actions for state """
        raise NotImplementedError
    def next_state(self, state, action):
        """ Abstract method that implements a transition function """
        raise NotImplementedError
    def is_goal_state(self, state):
        """ Abstract method that implements if a state reached a goal state """
        raise NotImplementedError
    def cost(self, state, action):
        """ Abstract method that implements the cost of transition """
        raise NotImplementedError


class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first"""
    def __init__(self, key, items=(),):
        self.key = key
        self.items = []  # a heap of (score, counter, item) pairs
        self.count = 0
        for item in items:
            self.add(item)


    def add(self, item):
        """ Add item to the queue """
        m_tuple = (self.key(item), self.count, item)
        self.count += 1
        heapq.heappush(self.items, m_tuple)


    def pop(self):
        """ Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[2]


    def top(self):
        """ Return the item on top of the PQ """
        return self.items[0][2]


    def __len__(self):
        return len(self.items)



def informed_search(problem, func):
    """ Informed search that uses func as key for the Priority Queue """
    initial_node = Node(problem.initial_state(), 0)
    frontier = PriorityQueue(func, [initial_node])
    reached = dict()
    reached[initial_node.state] = initial_node.cost
    while frontier:
        node = frontier.pop()
        if problem.is_goal_state(node.state):
            return node
        for action in problem.actions(node.state):
            state = problem.next_state(node.state, action)
            cost = problem.cost(node.state, action) + node.cost
            #frontier.add(Node(state, cost, node, action))
            if state not in reached or cost < reached[state]:
                reached[state] = cost
                frontier.add(Node(state, cost, node, action))
    return None


def uniform_cost_search(problem):
    """ Uniform cost search for a problem that is instance of Problem

        Function :func:'uniform_cost_search' executes an informed search
        on problem and returns None if the problem has no solution or
        a Node with a goal state for that problem.

        :param problem: A subclass of the Problem class
        :type problem: <subclass of 'Problem'>
        :return solution: A Node with a goal state or None if no solution.
        :rtype: <class 'Node'> or <class 'NoneType'>

        :Example:

        >>> goal = uniformCostSearch(problem)
        >>> goal.state
        (1,2,3,4,5,6,7,8,0)
        >>> goal.parent
        <__main__.node object at 0x7f29fbc301d0>
    """
    return informed_search(problem, lambda node: node.cost)


def a_star(problem, func):
    """ Implements the A* search for problem

        Executes an A* search over problem using func as the heuristics, or
        the key for the Priority Queue.
        It returns None if no solution exists or a Node with a goal state.

        :param problem: A subclass of the Problem class
        :type problem: <subclass of 'Problem'>
        :return solution: A Node with a goal state or None if no solution.
        :rtype: <class 'Node'> or <class 'NoneType'>

        :Example:

        >>> goal = a_star(problem, func)
        >>> goal.state
        (1,2,3,4,5,6,7,8,0)
        >>> goal.parent
        <__main__.node object at 0x7f29fbc301d0>
    """
    return informed_search(problem, func)


def deep_copy(*args):
    """ Auxiliary function to perform a deep copy

    Since python ``pass'' some values by reference and also make some
    attributions by reference (swallow copy), without performing a deep copy of
    some variables (like the grid matrix) we may face unexpected results by
    having another class/method/function messing up with our data

    Because of that, we provide you this auxiliary function to allow a
    friendly copy.deepcopy interface. However, you are completely free to use
    copy.deepcopy directly or even create your own deepcopy function/method

    :Example:

    >>> grid1 = [[1,2], [0,3]]
    >>> var1 = 10
    >>> var2 = 'OK'
    >>> sw_grid = grid1
    >>> sw_var1 = var1
    >>> sw_var2 = var2
    >>> dp_grid, dp_var1, dp_var2 = deep_copy(grid1, var1, var2)
    >>> grid1
    [[1, 2], [0, 3]]
    >>> sw_grid
    [[1, 2], [0, 3]]
    >>> dp_grid
    [[1, 2], [0, 3]]
    >>> grid1[0][0] = 1000
    >>> grid1
    [[1000, 2], [0, 3]]
    >>> sw_grid
    [[1000, 2], [0, 3]]
    >>> dp_grid
    [[1, 2], [0, 3]]
    """
    final_result = []
    for elem in args:
        new = copy.deepcopy(elem)
        final_result.append(new)
    return tuple(final_result)


class USPber(Problem):
    """ Implements the logic for the USPber game as a problem

    .. seealso::
        Check programming assignment for the game rules/definitions
    """
    def __init__(self, grid, **kwargs):
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = grid
        self.__agent1_faults = 0
        self.__agent2_faults = 0
        self.__agent1_gas_spent = 0
        self.__agent2_gas_spent = 0
        self.__agent1_gas_refilled = 0
        self.__agent2_gas_refilled = 0

        # change starting_turn if game starts in the middle
        self.__turn = kwargs.get('starting_turn', 1)
        # define if single or multi agent game
        self.multi_agent = kwargs.get('multi_agent', True)
        # By default taxis has the same tank capacity (INFTY if not defined)
        self.st_gas = kwargs.get('tank_capacity', INT_INFTY)
        # set bonusp1, bonusp2 and max_turns for test/debug only
        self.__agent1_people = kwargs.get('agent1_people', 0)
        self.__agent2_people = kwargs.get('agent2_people', 0)
        self.__max_turns = kwargs.get('max_turns', MAX_TURNS)


    def __player_pos(self, state):
        # Only queries, no need to deep copy here
        grid, turn, _, _, _, _ = state
        # In case of multi_agent: agent01 (codes 1 and 8) and agent02 (2 and 9)
        if self.multi_agent:
            if turn == 2:
                current_player = [2, 9]
            else:
                current_player = [1, 8]
        else:
            current_player = [1, 8]

        for i in range(self.height):
            for j in range(self.width):
                if grid[i][j] in current_player:
                    return (i, j)

        return None

    @staticmethod
    def __players_on_gas_station(grid):
        """ Auxiliar method to control if cars are on the gas_station

        This method check the grid to see if player1/player2 are inside a
        gas station and returns a boolean tuple with two values indicating
        which, if any, are inside the gas station
        """
        player1_on_gas = False
        player2_on_gas = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 8:
                    player1_on_gas = True
                elif grid[i][j] == 9:
                    player2_on_gas = True
        return (player1_on_gas, player2_on_gas)


    @staticmethod
    def __deep_copy(*args):
        final_result = []
        for elem in args:
            new = copy.deepcopy(elem)
            final_result.append(new)
        return tuple(final_result)


    def get_score(self, game_with_money=GAME_MONEY):
        """ Returns the score """
        if game_with_money:
            score = self.__agent1_people*MONEY_PER_BONUS
            score += self.__agent1_gas_spent*MONEY_PER_FUEL
            score += self.__agent1_faults*MONEY_PER_FAULT
            return score

        return self.__agent1_people


    def get_game_info(self, state):
        """ Returns the full info for a given state """
        grid, player, t01g, t02g, t01p, t02p = state
        full_info = {}
        full_info['agent1_people'] = t01p
        full_info['agent2_people'] = t02p
        full_info['agent1_faults'] = self.__agent1_faults
        full_info['agent2_faults'] = self.__agent2_faults
        full_info['agent1_gas_spent'] = self.__agent1_gas_spent
        full_info['agent2_gas_spent'] = self.__agent2_gas_spent
        full_info['agent1_remaing_gas'] = t01g
        full_info['agent2_remaing_gas'] = t02g
        full_info['agent1_gas_refilled'] = self.__agent1_gas_refilled
        full_info['agent2_gas_refilled'] = self.__agent2_gas_refilled
        full_info['game_final_grid'] = grid
        full_info['game_final_player'] = player
        full_info['game_total_turns'] = self.__turn
        return full_info


    def is_state(self, state):
        """ Simple state checking

        Do not check if state is reachable from start nor if immovables
        (e.g. gas, buildings) moved.
        State is a tuple with:
          0     1        2          3           4             5
        (grid, turn, taxi01gas, taxi02gas, taxi01people, taxi02people)
         """
        # Only queries, no need to deep copy here
        grid, turn, taxi01gas, taxi02gas, taxi01p, taxi02p = state

        if len(grid) != self.height or len(grid[0]) != self.width:
            return False
        if turn < 1 or turn > 2:  # Current USPber supports only 2 players
            return False
        if taxi01gas < 0 or taxi02gas < 0:  # Taxi cannot have negative fuel
            return False
        if taxi01p < 0 or taxi02p < 0:  # There is no negative bonus for people
            return False

        player01_found = False
        if self.multi_agent:
            player02_found = False
        else:
            player02_found = True

        for i in range(self.height):
            for j in range(self.width):
                if not isinstance(grid[i][j], int):
                    return False
                if grid[i][j] < 0 or grid[i][j] > 9:
                    return False
                if grid[i][j] == 1 or grid[i][j] == 8:
                    if player01_found:
                        return False
                    player01_found = True
                if grid[i][j] == 2 or grid[i][j] == 9:
                    if player02_found:
                        return False
                    player02_found = True
        return True


    def initial_state(self):
        initial = (self.grid, self.__turn, self.st_gas, self.st_gas,
                   self.__agent1_people, self.__agent2_people)
        return initial


    def actions(self, state):
        """ Returns the list of valid actions """

        player_pos = self.__player_pos(state)
        # Only queries, no need to deep copy here
        grid, _, taxi01gas, taxi02gas, _, _ = state
        i, j = player_pos

        player_number = grid[i][j]
        # Fix case where taxi is inside gas station
        if player_number > 2:
            what_player = player_number - 7
        else:
            what_player = player_number

        if what_player == 1:
            obstacles = [2, 5, 9]
            remaining_gas = taxi01gas
        else:
            obstacles = [1, 5, 8]
            remaining_gas = taxi02gas

        valid = []
        if remaining_gas > 0:
            if i+1 < self.height and grid[i+1][j] not in obstacles:
                valid.append('DOWN')
            if i-1 >= 0 and grid[i-1][j] not in obstacles:
                valid.append('UP')
            if j-1 >= 0 and grid[i][j-1] not in obstacles:
                valid.append('LEFT')
            if j+1 < self.width and grid[i][j+1] not in obstacles:
                valid.append('RIGHT')
        if grid[i][j] in [8, 9]:  # Who is in gas was already determined
            valid.append('REFILL')
        valid.append('STOP')  # STOP is always a valid action
        return valid


    #       0    1 2  3   4     5      6         7        8       9
    #args:p_flag,i,j,act,grid,turn,taxi01gas,taxi02gas,taxi01p,taxi02p
    def __update_all(self, *args):
        """ Private method to update board

        p-flag is just the current player minus 1 to allow comparison
        simplifications.
        Whoever calls __update_all can pass None as action if the action does
        not belong to the scope of USPber, in other words, if action not
        in aux. This allow the controller to deal with bad return from one
        or more agents.
        Whenever this occurs, the current player loses an unit of fuel.
        This is different from STOP where the player does not lose anything.
        However, if action in aux, it MUST be a valid action, otherwise the
        results are unexpected.
        """
        # Will operate over values, need to deep copy
        p_flag, i, j, action, grid, _, t1g, t2g, t1p, t2p = self.__deep_copy(*args)

        aux = {'UP'    : [i-1, j],
               'DOWN'  : [i+1, j],
               'LEFT'  : [i, j-1],
               'RIGHT' : [i, j+1],
               'STOP'  : [i, j],
               'REFILL': [i, j]}

        self.__turn += 1
        if action not in aux:
            if not p_flag:  # player01
                self.__agent1_faults += 1
                self.__agent1_gas_spent += 1
                if t1g > 0:
                    return (grid, 2, t1g-1, t2g, t1p, t2p)
                else:
                    return (grid, 2, t1g, t2g, t1p, t2p)
            else:
                self.__agent2_faults += 1
                self.__agent2_gas_spent += 1
                if t2g > 0:
                    return (grid, 1, t1g, t2g-1, t1p, t2p)
                else:
                    return (grid, 1, t1g, t2g, t1p, t2p)

        if action == 'STOP':
            if not p_flag:
                return (grid, 2, t1g, t2g, t1p, t2p)
            else:
                return (grid, 1, t1g, t2g, t1p, t2p)

        if action == 'REFILL':
            if not p_flag:
                if t1g + DEFAULT_REFILL < self.st_gas:  # Refill or max
                    self.__agent1_gas_refilled += DEFAULT_REFILL
                    t1g += DEFAULT_REFILL
                else:
                    self.__agent1_gas_refilled += self.st_gas - t1g
                    t1g = self.st_gas
                return (grid, 2, t1g, t2g, t1p, t2p)
            else:
                if t2g + DEFAULT_REFILL < self.st_gas:
                    self.__agent2_gas_refilled += DEFAULT_REFILL
                    t2g += DEFAULT_REFILL
                else:
                    self.__agent2_gas_refilled += self.st_gas - t2g
                    t2g = self.st_gas
                return (grid, 1, t1g, t2g, t1p, t2p)


        actual_cell = grid[i][j]
        future_cell = grid[aux[action][0]][aux[action][1]]
        # Process cell that taxi is leaving
        if actual_cell in [8, 9]:  # Leaving a gas station
            grid[i][j] = 4  # Revert to gas station and refill
        else:
            grid[i][j] = 0  # Not leaving gas, just empty cell

        # Process cell that taxi will arrive
        # Deal with complicated cases first, taxi going to gas station
        if future_cell == 4:
            grid[aux[action][0]][aux[action][1]] = (p_flag + 1) + 7
            if not p_flag:
                self.__agent1_gas_spent += 1
                return (grid, 2, t1g-1, t2g, t1p, t2p)
            else:
                self.__agent2_gas_spent += 1
                return (grid, 1, t1g, t2g-1, t1p, t2p)
        # Other cases taxi will fill that cell and only check if got people
        grid[aux[action][0]][aux[action][1]] = p_flag + 1
        if future_cell == 3:
            if not p_flag:
                t1p += STUDENT_BONUS
            else:
                t2p += STUDENT_BONUS
        elif future_cell == 6:
            if not p_flag:
                t1p += PROFESSOR_BONUS
            else:
                t2p += PROFESSOR_BONUS
        elif future_cell == 7:
            if not p_flag:
                t1p += MONITOR_BONUS
            else:
                t2p += MONITOR_BONUS
        # All possible bonus computed, just update turn and gas
        self.__agent1_people = t1p
        self.__agent2_people = t2p
        if not p_flag:
            self.__agent1_gas_spent += 1
            return (grid, 2, t1g-1, t2g, t1p, t2p)
        else:
            self.__agent2_gas_spent += 1
            return (grid, 1, t1g, t2g-1, t1p, t2p)


    def next_state(self, state, action):
        """ Transition state function for USPber """
        # If tried invalid action, reduce gas and stays in position
        # Changes will happen in __update_all, but deep copy here for safety
        c_grid, c_turn, c_t1g, c_t2g, c_t1p, c_t2p = state
        grid, turn, t1g, t2g, t1p, t2p = self.__deep_copy(c_grid, c_turn, c_t1g,
                                                          c_t2g, c_t1p, c_t2p)
        player_pos = self.__player_pos(state)
        i, j = player_pos
        what_player = grid[i][j]
        if what_player > 2:  # Fix case player in gas station
            what_player -= 7

        if action not in self.actions(state):
            return self.__update_all(what_player-1, i, j, None, grid, turn,
                                     t1g, t2g, t1p, t2p)

        return self.__update_all(what_player-1, i, j, action, grid, turn,
                                 t1g, t2g, t1p, t2p)


    def is_goal_state(self, state):
        grid, _, taxi01gas, taxi02gas, _, _ = state
        if taxi01gas < 1 and taxi02gas < 1:  # Both have empty tank
            p1_on_gas, p2_on_gas = self.__players_on_gas_station(grid)
            if not (p1_on_gas or p2_on_gas):
                return True
        if self.__turn > self.__max_turns:
            return True
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] in [3, 6, 7]:  # people, Denis or Decio
                    return False
        return True


    def cost(self, state, action):
        """ Returns infinity cost for invalid actions otherwise cost 1 """
        if action in self.actions(state):
            return 1
        return INT_INFTY
