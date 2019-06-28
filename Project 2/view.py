#!/usr/bin/python3
"""
########################################################################
#       Graphical interface for the USPber game (USP AI course)        #
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
import tkinter as tk
from tkinter import messagebox as tk_message
import sys
import random
import time
from PIL import Image, ImageTk


class View(object):
    """ Implements the GUI View component in the MVC architecture for EP2 """

    def __init__(self, controller, **kwargs):
        self.root = tk.Tk()
        self.root.title("MAC0425 AI Course (Programming assignment 02)")
        self.screen_width = self.root.winfo_screenwidth()/2
        self.screen_height = self.root.winfo_screenheight()/2
        self.controller = controller
        self.gridboard = kwargs['gridboard']

        n_row = len(self.gridboard)
        n_col = len(self.gridboard[0])

        if n_col/n_row > self.screen_width/self.screen_height:
            self.cell_size = (self.screen_width/n_col)-3
        else:
            self.cell_size = (self.screen_height/n_row)-3

        img_dim = int(self.cell_size*0.9)

        self.draw_delay = 0.5

        self.delay = kwargs.get('delay', 500)

        try:
            preproc_random = [
                Image.open('random01.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('random02.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('random03.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('random04.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('random05.jpg').resize((img_dim, img_dim), Image.ANTIALIAS)]

            self.people = []
            for img in preproc_random:
                self.people.append(ImageTk.PhotoImage(img))

            preproc_building = [
                Image.open('building01.png').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('building02.png').resize((img_dim, img_dim), Image.ANTIALIAS)]

            preproc_monitor = [
                Image.open('decio.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('julissa.jpg').resize((img_dim, img_dim), Image.ANTIALIAS),
                Image.open('fabio.jpg').resize((img_dim, img_dim), Image.ANTIALIAS)]

            self.monitors = []

            for img2 in preproc_monitor:
                self.monitors.append(ImageTk.PhotoImage(img2))

            self.decio = preproc_monitor[0]

            self.buildings = []

            for img3 in preproc_building:
                self.buildings.append(ImageTk.PhotoImage(img3))

            #preproc_decio = Image.open('decio.jpg')
            #preproc_decio = preproc_decio.resize((img_dim, img_dim), Image.ANTIALIAS)
            #self.decio = ImageTk.PhotoImage(preproc_decio)

            preproc_denis = Image.open('denis.jpg')
            preproc_denis = preproc_denis.resize((img_dim, img_dim), Image.ANTIALIAS)
            self.denis = ImageTk.PhotoImage(preproc_denis)
            self.professors = [self.denis]

            preproc_taxi01 = Image.open('taxi_yellow.png')
            preproc_taxi01 = preproc_taxi01.resize((img_dim, img_dim), Image.ANTIALIAS)
            self.taxi01 = ImageTk.PhotoImage(preproc_taxi01)

            preproc_taxi02 = Image.open('taxi_black.png')
            preproc_taxi02 = preproc_taxi02.resize((img_dim, img_dim), Image.ANTIALIAS)
            self.taxi02 = ImageTk.PhotoImage(preproc_taxi02)

            preproc_our_taxi = Image.open('ferrari.png')
            preproc_our_taxi = preproc_our_taxi.resize((img_dim, img_dim), Image.ANTIALIAS)
            self.our_taxi = ImageTk.PhotoImage(preproc_our_taxi)

            preproc_gas = Image.open('fuel.png')
            preproc_gas = preproc_gas.resize((img_dim, img_dim), Image.ANTIALIAS)
            self.gas = ImageTk.PhotoImage(preproc_gas)

        except IOError as exc:
            print("Unable to open image files: {0}".format(exc))
            sys.exit(1)
        except Exception as exc:
            print("Unexpected error while processing images: {0}".format(exc))
            sys.exit(1)

        self.__create_menu_bar()

        self.__create_canvas(canvas_width=self.screen_width, canvas_height=self.screen_height)

        self.__bottom_bar()

        self.__process_board(self.gridboard)

        self.update(self.gridboard, [0, 0])


    def __bottom_bar(self):
        self.less_delay = tk.Button(self.root, bg="gray70")
        self.less_delay["text"] = "-"
        self.less_delay.bind("<Button-1>", self.__minus_delay_button)
        self.less_delay.pack(side="left")

        self.delay_value = tk.Label(self.root, text=str(self.draw_delay))
        self.delay_value["font"] = ("Arial", "10", "bold")
        self.delay_value.pack(side="left")

        self.plus_delay = tk.Button(self.root, bg="gray70")
        self.plus_delay["text"] = "+"
        self.plus_delay.bind("<Button-1>", self.__plus_delay_button)
        self.plus_delay.pack(side="left")

        self.delay_value = tk.Label(self.root, text="  ")
        self.delay_value.pack(side="left")

        self.step = tk.Button(self.root, bg="gray")
        self.step["text"] = "step"
        self.step.bind("<Button-1>", self.__step_button)
        self.step.pack(side="left")

        self.full_game = tk.Button(self.root, bg="gray")
        self.full_game["text"] = "play"
        self.full_game.bind("<Button-1>", self.__full_game_button)
        self.full_game.pack(side="left")


        self.pontuation = tk.Label(self.root, text="Player 1: 0 \t Player 2: 0")
        self.pontuation["font"] = ("Arial", "10", "bold")
        self.pontuation.pack(side="right")


    def __step_button(self, _):
        self.controller.step_graphical(self)
        self.root.update()


    def __full_game_button(self, _):
        self.step["state"] = 'disabled'
        self.full_game["state"] = 'disabled'
        score = None
        while not score:
            score = self.controller.step_graphical(self)
            self.root.update()
            time.sleep(self.draw_delay)


    def __plus_delay_button(self, _):
        if self.draw_delay < 1.5:
            self.draw_delay += 0.1
            self.draw_delay = round(self.draw_delay, 1)
        self.delay_value["text"] = str(self.draw_delay)


    def __minus_delay_button(self, _):
        if self.draw_delay > 0.1:
            self.draw_delay -= 0.1
            self.draw_delay = round(self.draw_delay, 1)
        self.delay_value["text"] = str(self.draw_delay)


    def print_results(self, full_info, game_with_money=False):
        """ Print a friendly summary for both score modes """
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
        if not game_with_money:
            score = p1p
        else:
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
Final score: {12}""".format(p1p, p1s, p1rf, p1rg, p1f, p2p, p2s, p2rf, p2rg,
                            p2f, last_player, turns, score)
        tk_message.showinfo("Game summary", friendly_score)
        self.root.destroy()
        sys.exit(0)


    def __create_menu_bar(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        menu_file = tk.Menu(self.menu_bar)
        menu_file.add_command(label="Export Game", command=self.__export)
        menu_file.add_command(label="Import Game", command=self.__import)
        menu_file.add_command(label="Quit", command=self.__view_exit)
        self.menu_bar.add_cascade(label="File", menu=menu_file)

        menu_help = tk.Menu(self.menu_bar)
        menu_help.add_command(label="Help", command=self.__print_help)
        menu_help.add_command(label="About", command=self.__print_about)
        self.menu_bar.add_cascade(label="Help", menu=menu_help)


    def __create_canvas(self, **kwargs):
        if len(kwargs) > 1:
            width = kwargs['canvas_width']
            height = kwargs['canvas_height']
            if 'background' in kwargs:
                background = kwargs['background']
            else:
                background = "grey"
        else:
            raise ValueError("Canvas need at least width and height")
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.configure(background=background)
        self.canvas.pack()


    def __process_board(self, gridboard):
        """ Board code:
        0: Empty cell
        1: Taxi01
        2: Taxi02
        3: Random_person
        4: Gas station
        5: Obstacle (building)
        6: Denis
        7: Decio
        8: Taxi01 parked in gas station
        9: Taxi02 parked in gas station
        """
        self.people_pos = {}
        self.building_pos = {}
        self.monitors_pos = {}
        self.professors_pos = {}
        for row in range(len(gridboard)):
            for col in range(len(gridboard[0])):
                if gridboard[row][col] == 3:
                    self.people_pos[(row, col)] = random.choice(self.people)
                elif gridboard[row][col] == 5:
                    self.building_pos[(row, col)] = random.choice(self.buildings)
                elif gridboard[row][col] == 6:
                    self.professors_pos[(row, col)] = random.choice(self.professors)
                elif gridboard[row][col] == 7:
                    self.monitors_pos[(row, col)] = random.choice(self.monitors)


    def __export(self):
        tk_message.showinfo("Export Game", "Not implemented yet")


    def __import(self):
        tk_message.showinfo("Import Game", "Not implemented yet")


    def __view_exit(self):
        self.root.destroy()
        sys.exit(0)


    def __print_help(self):
        help_win = tk.Toplevel()
        help_win.title('Help')
        help_win.geometry("500x350")
        help_message = """
           Graphical interface for the USPber game.


Menus:
File->Export Game: Export the list of actions. (Will be saved into game.txt)
File->Import Game: Read a valid exported game.txt and execute it.
File->Quit: Exit the game.
Help->Help: Display this message.
Help->About: Display license and complementary info.

Interface:
+ or - Buttons: Controls the game simulation/rendering speed
Step Button: Execute a single turn.
Play Button: Runs the entire game to the end.
Player1: Shows the current score for the first player
Player2: Shows the current score for the second player
"""
        tk.Label(help_win, text=help_message, anchor='w', justify='left').pack()
        tk.Button(help_win, text='Close', command=help_win.destroy).pack()


    def __print_about(self):
        about_win = tk.Toplevel()
        about_win.title('About')
        about_win.geometry("500x350")
        about_message = """
       Graphical interface for the USPber game (USP AI course)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

(C) Copyright 2019 Denis Deratani Maua (denis.maua@usp.br)
(C) Copyright 2019 Decio Lauro Soares (deciolauro@gmail.com)
(C) Copyright 2019 Fabio Henrique Tanaka (fhktanaka@gmail.com)
(C) Copyright 2019 Julissa Villanueva Llerena (jgville@ime.usp.br)
"""
        tk.Label(about_win, text=about_message, anchor='w', justify='left').pack()
        tk.Button(about_win, text='Close', command=about_win.destroy).pack()


    def redraw(self):
        """ Update tasks and redraw canvas after delay """
        self.root.update_idletasks()
        self.root.after(self.delay, self.redraw)


    def update(self, board, pontuation, **kwargs):
        """ Update control for redraw """
        self.draw_and_update(board, pontuation, **kwargs)


    def draw_and_update(self, board, score, **kwargs):
        """ Process board and score and call relevant methods """
        n_row = len(board)
        n_col = len(board[0])
        def_margin = 5
        def_delay = 350
        def_left = (self.screen_width-(self.cell_size*n_col))/2
        def_right = def_left + self.cell_size
        def_top = (self.screen_height-(self.cell_size*n_row))/2
        def_bottom = def_top + self.cell_size

        final_options = {'margin': def_margin,
                         'cell_size': self.cell_size,
                         'grid_left': def_left,
                         'grid_right': def_right,
                         'grid_top': def_top,
                         'grid_bottom': def_bottom,
                         'delay': def_delay
                        }

        for option in final_options:
            if option in kwargs:
                final_options[option] = kwargs[option]

        self.canvas.delete("all")
        for row in range(n_row):
            for col in range(n_col):
                self.__draw_cell(final_options, board[row][col], row, col)

        self.root.after(final_options['delay'], self.redraw)
        self.pontuation["text"] = "Player 1: {} \t Player 2: {}".format(score[0],
                                                                        score[1])


    def __draw_cell(self, options, item, row, col):
        colors = ("#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
                  "#FFFFFF", "#FEE101", "#C0C0C0", "#FFA500", "#FFA500")
        if item == 3 and (row, col) not in self.people_pos:
            self.people_pos[(row, col)] = random.choice(self.people)
        elif item == 5 and (row, col) not in self.building_pos:
            self.building_pos[(row, col)] = random.choice(self.buildings)
        elif item == 6 and (row, col) not in self.professors_pos:
            self.professors_pos[(row, col)] = random.choice(self.professors)
        elif item == 7 and (row, col) not in self.monitors_pos:
            self.monitors_pos[(row, col)] = random.choice(self.monitors)

        if (row, col) in self.people_pos:
            images = (None, self.taxi01, self.taxi02,
                      self.people_pos[(row, col)],
                      self.gas, None, self.denis,
                      self.decio, self.taxi01, self.taxi02)
        elif (row, col) in self.building_pos:
            images = (None, self.taxi01, self.taxi02,
                      None, self.gas, self.building_pos[(row, col)],
                      self.denis, self.decio, self.taxi01, self.taxi02)
        elif (row, col) in self.monitors_pos:
            images = (None, self.taxi01, self.taxi02,
                      None, self.gas, None, self.denis,
                      self.monitors_pos[(row, col)], self.taxi01, self.taxi02)
        elif (row, col) in self.professors_pos:
            images = (None, self.taxi01, self.taxi02,
                      None, self.gas, None, self.professors_pos[(row, col)],
                      self.decio, self.taxi01, self.taxi02)
        else:
            images = (None, self.taxi01, self.taxi02, None, self.gas,
                      None, self.denis, self.decio, self.taxi01, self.taxi02)

        if item < 0:
            self.canvas.create_rectangle(
                options['grid_left']+col*options['cell_size'],
                options['grid_top']+row*options['cell_size'],
                options['grid_right']+col*options['cell_size'],
                options['grid_bottom']+row*options['cell_size'],
                fill=colors[0])
        else:
            self.canvas.create_rectangle(
                options['grid_left']+col*options['cell_size'],
                options['grid_top']+row*options['cell_size'],
                options['grid_right']+col*options['cell_size'],
                options['grid_bottom']+row*options['cell_size'],
                fill=colors[item])
        if item > 0 and item < 10:
            self.canvas.create_image(
                options['grid_left']+(col*options['cell_size'])+options['cell_size']/2,
                options['grid_top']+(row*options['cell_size'])+options['cell_size']/2,
                anchor=tk.CENTER,
                image=images[item])
