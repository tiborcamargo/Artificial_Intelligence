#!/usr/bin/python3
"""
########################################################################
#       Game controller for the USPber gamea (USP AI course)           #
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
import util
import view
import ep2


class GameControlller:
    """ Implements the Controller in the MVC architectural pattern """

    def __init__(self, problem, agent1, agent2, **kwargs):
        """ During the initialization, this class receives

        :param problem: An instantiated subclass of Problem with the problem
            definition from the perspective of the game (e.g. USPber)
        :param agent1: An instantiated subclass of Agent with the agent
            for the first player
        :param agent2: An instantiated subclass of Agent with the agent
            for the second player
        :type problem: subclass of <class 'Problem'>
        :type agent1: subclass of <class 'Agent'>
        :type agent2: subclass of <class 'Agent'>

        :Example:

        >>> grid_example = [[1,0,4,2], [7,5,5,0], [3,4,5,4], [0,0,6,3]]
        >>> problem = util.USPber(grid=grid_example, multi_agent=True,
        ... tank_capacity=6)
        >>> agent1 = ep2.RandomAgent(player_number=1, number_of_agents=1,
        ... tank_capacity=6)
        >>> agent2 = ep2.DoNothingAgent(player_number=2, tank_capacity=6)
        >>> ctrl = GameControlller(problem, agent1, agent2)
        """
        self.problem = problem
        self.agent1 = agent1
        self.agent2 = agent2
        self.state = problem.initial_state()
        self.tank_capacity = self.problem.st_gas
        # Debug/Autograder ONLY!
        self.turn = kwargs.get('turn', 0)
        self.actions = kwargs.get('actions_list', [])
        if 'initial_perception_list' in kwargs:
            self.state1 = kwargs['initial_perception_list'][0]
            self.state2 = kwargs['initial_perception_list'][1]
        else:
            state1 = problem.initial_state()
            grid, _, taxi01gas, taxi02gas, _, _ = state1
            # All information that any Agent perceives from the world is:
            # A tuple with the entire grid and their remaing fuel
            self.state1 = (grid, taxi01gas)
            self.state2 = (grid, taxi02gas)


    def step_graphical(self, current_view):
        """ Process a turn for the current agent and renders it in view """

        # IMPORTANT: The logic must be changed for more than 2 agents
        if self.turn % 2 == 0:
            act = self.agent1.get_action(self.state1)
            cur_player = 1
        else:
            act = self.agent2.get_action(self.state2)
            cur_player = 2


        self.state = self.problem.next_state(self.state, act)
        n_grid, _, nt01g, nt02g, nt01p, nt02p = self.state

        if util.SHOW_INFO:
            print("********************")
            score = self.problem.get_score()
            info = "Player {0} choosed action: {1}, score: {2}".format(cur_player,
                                                                       act,
                                                                       score)
            print(info)
            for line in n_grid:
                print(line)
            print("********************")
        self.state1 = (n_grid, nt01g)
        self.state2 = (n_grid, nt02g)
        self.turn += 1
        self.actions.append(act)

        current_view.update(n_grid, [nt01p, nt02p])

        if self.problem.is_goal_state(self.state):
            print("Game Ended")
            if util.SHOW_INFO:
                grid, _, _, _, _, _ = self.state
                for line in grid:
                    print(line)

            score = self.problem.get_score()
            final_info = self.problem.get_game_info(self.state)
            if util.SHOW_INFO:
                self.print_friendly_summary(final_info)
            else:
                print("Final score: {0}".format(score))
            current_view.print_results(final_info, util.GAME_MONEY)
            return score
        return None


    @staticmethod
    def print_friendly_summary(full_info, game_with_money=util.GAME_MONEY):
        """ Prints a friendly summary with game info for both score types """
        p1p = full_info['agent1_people']
        p1s = full_info['agent1_gas_spent']
        p1rf = full_info['agent1_gas_refilled']
        p1rg = full_info['agent1_remaing_gas']
        p1f = full_info['agent1_faults']
        p2p = full_info['agent2_people']
        p2s = full_info['agent2_gas_spent']
        p2rf = full_info['agent2_gas_refilled']
        p2rg = full_info['agent2_remaing_gas']
        p2f = full_info['agent2_faults']
        last_player = full_info['game_final_player']
        turns = full_info['game_total_turns']
        if not game_with_money:  # Score1: Just collected by player1 matters
            score = p1p
        else:  # Score2: Money associated with p1 collected, fuel and faults
            score = 10*p1p - 2*p1s - 20*p1f
        friendly_score = """
********************
Agent 01 Summary
********************
People bonus: {0}
Fuel spent: {1}
Fuel refilled: {2}
Fuel remaining: {3}
Faults committed: {4}
********************
Agent 02 Summary
********************
People bonus: {5}
Fuel spent: {6}
Fuel refilled: {7}
Fuel remaining: {8}
Faults committed: {9}
********************
Game info
********************
Last agent: {10}
Number of turns: {11}
Final score: {12}""".format(p1p, p1s, p1rf, p1rg, p1f,
                            p2p, p2s, p2rf, p2rg, p2f,
                            last_player, turns, score)
        print(friendly_score)


    def step_terminal(self, show_info=True):
        """ Execute a single turn (terminal mode) """
        # IMPORTANT: The logic must be changed for more than 2 agents
        if self.turn % 2 == 0:
            act = self.agent1.get_action(self.state1)
            cur_player = 1
        else:
            act = self.agent2.get_action(self.state2)
            cur_player = 2

        self.state = self.problem.next_state(self.state, act)
        n_grid, _, nt01g, nt02g, _, _ = self.state
        self.state1 = (n_grid, nt01g)
        self.state2 = (n_grid, nt02g)
        self.turn += 1
        self.actions.append(act)

        if show_info:
            score = self.problem.get_score()
            info = "Agent {0} choosed action: {1}, score: {2}".format(cur_player,
                                                                      act,
                                                                      score)
            print(info)
            for line in n_grid:
                print(line)

        if self.problem.is_goal_state(self.state):
            print("Game Ended")
            if show_info:
                grid, _, _, _, _, _ = self.state
                for line in grid:
                    print(line)
            score = self.problem.get_score()
            final_info = self.problem.get_game_info(self.state)
            if show_info:
                self.print_friendly_summary(final_info)
            else:
                print("Final score: {0}".format(score))
            return score
        return None


def run_terminal(grid_start, agent1=ep2.RandomAgent, agent2=ep2.RandomAgent):
    """ Runs a entire game in terminal mode """
    tank = util.TANK_CAPACITY
    problem = util.USPber(grid=grid_start,
                          multi_agent=True,
                          tank_capacity=tank)
    pl1 = agent1(player_number=1, number_of_agents=2,
                 tank_capacity=tank, max_depth=util.MAX_DEPTH)
    pl2 = agent2(player_number=2, number_of_agents=2,
                 tank_capacity=tank, max_depth=util.MAX_DEPTH)

    if util.SHOW_INFO:
        print("********************")
        print("   Starting game    ")
        print("********************")
        print("Initial board")
        for line in grid_start:
            print(line)

    ctrl = GameControlller(problem, pl1, pl2)

    score = None
    while score is None:
        score = ctrl.step_terminal(show_info=util.SHOW_INFO)


def run_view(grid_start, agent1=ep2.RandomAgent, agent2=ep2.RandomAgent):
    """ Runs a game in the graphical mode """
    tank = util.TANK_CAPACITY
    problem = util.USPber(grid=grid_start,
                          multi_agent=True,
                          tank_capacity=tank)
    pl1 = agent1(player_number=1, number_of_agents=2,
                 tank_capacity=tank, max_depth=util.MAX_DEPTH)
    pl2 = agent2(player_number=2, number_of_agents=2,
                 tank_capacity=tank, max_depth=util.MAX_DEPTH)

    if util.SHOW_INFO:
        print("********************")
        print("   Starting game    ")
        print("********************")
        print("Initial board")
        for line in grid_start:
            print(line)

    ctrl = GameControlller(problem, pl1, pl2)

    game_view = view.View(controller=ctrl, gridboard=grid_start)
    game_view.root.mainloop()



if __name__ == '__main__':
    import grid_generator
    # Change the following lines to switch between Agents
	# Some agents: GetClosestPersonOrRefillAgent, RandomAgent, AlphaBetaAgent, DoNothingAgent, CollectAllAgent
    Player1 = ep2.GetClosestPersonOrRefillAgent
    Player2 = ep2.AlphaBetaAgent

    # Change the following matrix to start a different game
    GAME_GRID = grid_generator.generate_random_grid()
#    GAME_GRID = [[1, 3, 0, 3],
#                 [7, 5, 4, 2],
#                 [3, 0, 6, 0]]

    if util.SHOW_DISPLAY:
        run_view(GAME_GRID, Player1, Player2)
    else:
        run_terminal(GAME_GRID, Player1, Player2)
