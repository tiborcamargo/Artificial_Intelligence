#!/usr/bin/python3
"""
########################################################################
#      Game positions generator for USPber game (USP AI course)        #
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
import random
import math

def generate_random_grid(**kwargs):
    """ Helper function to allow creation of your own grids

    Allow the creation of a random USPber grids.
    This function requires that you provide the percentage of occurrence for
    all elements in the grid, along with the size of the grid (width and height)
    You have to pass inside the kwargs argument the following parameters:

    Required:
        width = kwargs['width']              -> Default: 5
        height = kwargs['height']            -> Default: 4
        student_percentage = kwargs['sp']    -> Default: 0.3  (6 students)
        building_percentage = kwargs['bp']   -> Default: 0.1  (2 buildings)
        gas_percentage = kwargs['gp']        -> Default: 0.1  (2 gas)
        monitor_percentage = kwargs['mp']    -> Default: 0.1  (2 monitors)
        professor_percentage = kwargs['pp']  -> Default: 0.05 (1 professor)

    Board code:
        0: Empty cell
        1: Taxi01
        2: Taxi02
        3: Random_person
        4: Gas station
        5: Obstacle (building)
        6: Denis
        7: Decio
        8: Car 1 in gas station
        9: Car 2 in gas station

    .. Examples::

    >>> new_grid = generate_random_grid(width=5, height=6, sp=0.3, bp=0.1,
    ... gp=0.1, mp=0.1, pp=0.05)
    >>> new_grid
    [[4, 3, 4, 0, 3],
     [7, 5, 0, 5, 0],
     [3, 3, 3, 3, 1],
     [7, 5, 3, 3, 7],
     [0, 0, 4, 3, 0],
     [2, 0, 0, 6, 0]]
    >>> new_grid = generate_random_grid(width=5, height=6, sp=0.3, bp=0.1,
    ... gp=0.1, mp=0.1, pp=0.05)
    >>> new_grid
    [[3, 0, 3, 0, 0],
     [3, 2, 3, 4, 4],
     [0, 5, 4, 0, 0],
     [0, 7, 7, 0, 5],
     [3, 3, 0, 1, 5],
     [3, 6, 7, 3, 3]]
    >>> new_grid = generate_random_grid(width=5, height=6, sp=0.3, bp=0.1,
    ... gp=0.1, mp=0.1, pp=0.05)
    [[0, 0, 3, 8, 5],
     [3, 7, 0, 3, 0],
     [0, 2, 7, 0, 3],
     [6, 0, 3, 4, 0],
     [3, 5, 7, 3, 4],
     [5, 3, 3, 0, 0]]
    """
    width = kwargs.get('width', 5)
    height = kwargs.get('height', 4)
    total_cells = width*height
    # Check if percentage is valid
    student_percentage = kwargs.get('sp', 0.3)
    building_percentage = kwargs.get('bp', 0.1)
    gas_percentage = kwargs.get('gp', 0.1)
    monitor_percentage = kwargs.get('mp', 0.1)
    professor_percentage = kwargs.get('pp', 0.05)

    student_to_put = math.floor(total_cells*student_percentage)
    building_to_put = math.floor(total_cells*building_percentage)
    gas_to_put = math.floor(total_cells*gas_percentage)
    monitor_to_put = math.floor(total_cells*monitor_percentage)
    professor_to_put = math.floor(total_cells*professor_percentage)

    empty_cells = total_cells - (student_to_put + building_to_put + gas_to_put)
    empty_cells -= (monitor_to_put + professor_to_put + 2)
    if empty_cells < 0:
        raise ValueError("Unable to fit given percentage in the grid")

    c_l = empty_cells*[0]
    c_l += student_to_put*[3]
    c_l += building_to_put*[5]
    c_l += professor_to_put*[6]
    c_l += monitor_to_put*[7]

    if gas_to_put < 2:
        c_l += [1, 2]
    else:
        # Random selection to see if player1 or player2 starts in a gas station
        # 0.00 <= r < 0.25 -> both players start on gas stations
        # 0.25 <= r < 0.50 -> just player 1
        # 0.50 <= r < 0.75 -> just player 2
        # 0.75 <= r < 1,00 -> neither
        rollete = random.random()
        if rollete < 0.25:
            c_l += [8, 9]
            gas_to_put -= 2
        elif rollete < 0.5:
            c_l += [8, 2]
            gas_to_put -= 1
        elif rollete < 0.75:
            c_l += [1, 9]
            gas_to_put -= 1
        else:
            c_l += [1, 2]
    c_l += gas_to_put*[4]

    # Safety check
    if len(c_l) < total_cells:
        c_l += (total_cells-len(c_l))*[0]

    random.shuffle(c_l)

    final_grid = [[0]*width for _ in range(height)]

    for i in range(height):
        for j in range(width):
            final_grid[i][j] = c_l.pop()
    return final_grid


def generate_grid_from_sparce(**kwargs):
    """ Helper function to allow creation of your own grids

    Allow the creation of a specific USPber grids.
    This function requires that you provide the coordinates for all elements
    along with the size of the grid (width and height)
    You have to pass inside the kwargs argument the following parameters:

    width = kwargs['width']            -> Default: 5
    height = kwargs['height']          -> Default: 4
    student_positions = kwargs['sp']
    building_positions = kwargs['bp']
    gas_positions = kwargs['gp']
    monitor_positions = kwargs['mp']
    professor_positions = kwargs['pp']

    Required:
    player01_position = kwargs['p1p']
    player02_position = kwargs['p2p']

    Board code:
        0: Empty cell
        1: Taxi01
        2: Taxi02
        3: Random_person
        4: Gas station
        5: Obstacle (building)
        6: Denis
        7: Decio
        8: Car 1 in gas station
        9: Car 2 in gas station

    .. Example::

    >>> new_grid = generate_grid_from_sparce(width=8, height=10, p1p=(0,0),
    ... p2p=(2,3), sp=[(1,1), (2,2)], bp=[(3,3), (5,5)], gp=[(6,6), (0,4)],
    ... mp=[(5,4), (7,0)], pp=[(4,4)])
    >>> new_grid
    [[1, 0, 0, 0, 4, 0, 0, 0],
     [0, 3, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 2, 0, 0, 0, 0],
     [0, 0, 0, 5, 0, 0, 0, 0],
     [0, 0, 0, 0, 6, 0, 0, 0],
     [0, 0, 0, 0, 7, 5, 0, 0],
     [0, 0, 0, 0, 0, 0, 4, 0],
     [7, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0]]
    >>> new_grid = generate_grid_from_sparce(width=4, height=3, p1p=(0,0),
    ... p2p=(2,3), sp=[(1,1), (2,2)], gp=[(2,3)])
    >>> new_grid
    [[1, 0, 0, 0], [0, 3, 0, 0], [0, 0, 3, 9]]

    .. bugs::
        Does not verify if passed coordinate is inside the grid and may
        raise index error.
    """
    if 'p1p' not in kwargs or 'p2p' not in kwargs:
        raise ValueError("You must pass at least the position of both players")

    width = kwargs.get('width', 5)
    height = kwargs.get('height', 4)
    # Check if percentage is valid
    student_positions = kwargs.get('sp', [])
    building_positions = kwargs.get('bp', [])
    gas_positions = kwargs.get('gp', [])
    monitor_positions = kwargs.get('mp', [])
    professor_positions = kwargs.get('pp', [])

    final_grid = [[0]*width for _ in range(height)]

    for i, j in student_positions:
        final_grid[i][j] = 3
    for i, j in gas_positions:
        if final_grid[i][j] != 0:
            raise ValueError("Gas station conflict")
        final_grid[i][j] = 4
    for i, j in building_positions:
        if final_grid[i][j] != 0:
            raise ValueError("Building conflict")
        final_grid[i][j] = 5
    for i, j in monitor_positions:
        if final_grid[i][j] != 0:
            raise ValueError("Monitor conflict")
        final_grid[i][j] = 7
    for i, j in professor_positions:
        if final_grid[i][j] != 0:
            raise ValueError("Professor conflict")
        final_grid[i][j] = 6
    i, j = kwargs['p1p']
    if final_grid[i][j] != 0:
        if final_grid[i][j] == 4:
            final_grid[i][j] = 8
        else:
            raise ValueError("Player 1 conflict")
    else:
        final_grid[i][j] = 1

    i, j = kwargs['p2p']
    if final_grid[i][j] != 0:
        if final_grid[i][j] == 4:
            final_grid[i][j] = 9
        else:
            raise ValueError("Player 2 conflict")
    else:
        final_grid[i][j] = 2

    return final_grid
