# coding=utf-8
"""Definitions for the game."""
import os

import errno

from snake.gui import GameWindow
from snake.map import Direc, Pos, PointType, Map, Snake
# noinspection PyUnresolvedReferences
from snake.solver import HamiltonSolver, GreedySolver


class GameConfig:
    """
    Configuration for the game UI.
    """

    def __init__(self):
        # Size #
        self.map_rows = 10
        self.map_cols = self.map_rows
        self.map_width = 500  # pixels
        self.map_height = self.map_width
        self.info_panel_width = 170  # pixels
        self.window_width = self.map_width + self.info_panel_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.25

        # AI #
        self.enable_AI = False
        self.solver_name = 'GreedySolver'
        # This isn't very important since the solver type is changed in the run_script.

        # Visuals #
        self.show_gui = True
        # Enable show_gui to see a visual representation of the snake.
        # Disable it to do tests for consistency and accuracy.
        self.show_grid_line = True
        # Enable show_grid_line to draw grid lines, and vice-versa.
        self.show_info_panel = True
        # Enable show_info_panel to get information about the current solver,
        # the length of the snake, as well as other miscellaneous information.
        self.picture_logging = False
        # Enable this to log the position of the snake at every step. Slows down performance.

        # Delay #
        self.interval_draw = 40  # ms
        self.interval_draw_max = 200  # ms

        # Color #
        self.colour_bg = '#000000'  # Black
        self.colour_txt = '#F5F5F5'  # Close to white, but not entirely.
        self.colour_line = '#424242'  # Gray. Or is it grey?
        self.colour_wall = '#F5F5F5'  # Close to white.
        self.colour_food = '#FFF59D'  # A light shade of yellow.
        self.colour_head = '#F5F5F5'  # Close to white.
        self.colour_body = '#F5F5F5'  # Close to white.

        # Initial snake #
        self.init_direc = Direc.RIGHT
        # This is so that the snake position is not randomized.
        # The next direction of the snake is still none, so the snake will not move.
        self.init_bodies = [Pos(1, 2), Pos(1, 1)]
        # Set the initial positions of the snakes and the appearance of their bodies.
        self.init_types = [PointType.HEAD_R, PointType.BODY_HOR]

        # Font #
        self.font_info = ('Helvetica', 9)

        # Info #
        self.info_str = (
                "<w/a/s/d>: up/left/down/right\n"
                "<space>: pause/resume\n"
                "<r>: restart    <esc>: exit\n"
                "---------------------------------\n"
                "solver: %s\n"
                "status: %s\n"
                "steps: %d\n"
                "length: %d/%d (" + str(self.map_rows) + "x" + str(self.map_cols) + ")\n"
                # @formatter:off
                "---------------------------------\n"
                "move delay:"
                # @formatter:on
        )
        self.info_status = ['eating', 'dead', 'full']  # The different statuses for the snake. Very polar, I know.


class Game:
    """
    Game. Where all the functions are processed.
    You can run it without or with a gui.
    """

    def __init__(self, conf):
        self.__conf = conf
        self.__map = Map(conf.map_rows + 2, conf.map_cols + 2)  # The extra two rows and columns are for the walls.
        self.__snake = Snake(self.__map, conf.init_direc, conf.init_bodies, conf.init_types)
        self.__pause = False
        self.__window = GameWindow(conf,
                                   self.__map,
                                   "Snake",
                                   self.__snake,
                                   self.__on_exit,
                                   (
                                       ('<w>', lambda e: self.__update_direc(Direc.UP)),
                                       ('<a>', lambda e: self.__update_direc(Direc.LEFT)),
                                       ('<s>', lambda e: self.__update_direc(Direc.DOWN)),
                                       ('<d>', lambda e: self.__update_direc(Direc.RIGHT)),
                                       ('<r>', lambda e: self.__reset()),
                                       ('<space>', lambda e: self.__toggle_pause())
                                   )
                                   )
        self.__solver = globals()[self.__conf.solver_name](self.__snake)
        # By importing both the HamiltonSolver and the GreedySolver into the module,
        # we can freely access them from this module using the globals function.
        self.__episode = 1
        # This is for non-gui logging.
        self.__init_log_file()
        # Open log files.

    def run(self):
        """
        Main method. This is the only method called from outside the object.
        If gui is enabled, then the gui is called upon to start the loop with self.game_main.
        Otherwise, no gui is shown, and the program runs tests on the snakes.
        :return: None.
        """
        if self.__conf.show_gui:
            self.__window.show(self.__game_main)
            # Self.__game_main is passed as an argument to this argument to loop it using tkinter after and recursion.
        else:
            self.__run_batch_episodes()

    def __run_batch_episodes(self):
        """
        Main method for running batches of episodes at once.
        First the method gets the number of episodes to run.
        Then for each episodes, it simulates a full game, and logs the result.
        At the end, it prints out the total number of episodes, the total number of successful episodes,
        the average success rate, and the average number of steps taken to achieve victory.
        :return: None.
        """
        steps_limit = self.__map.capacity * 100
        episodes = self.__get_positive_integer('Please enter the amount of episodes: ')

        print('\nMap size: {}x{}'.format(self.__conf.map_rows, self.__conf.map_cols))
        print('Solver: {}\n'.format(self.__conf.solver_name[:-6].lower()))

        tot_suc, tot_suc_steps = 0, 0
        # Initialize the total number of successes,
        # and the sum of the number of steps taken for each success.
        for _ in range(episodes):  # Underscore is used to show that the episode number is not important.
            print('Episode {} - '.format(self.__episode), end='')
            while True:
                # Constantly run the game until the snake is either dead,
                # the map is full, or the snake has entered an infinite loop,
                # at which point the episode will report a fail.
                self.__game_main()
                if self.__map.is_full():
                    tot_suc += 1
                    tot_suc_steps += self.__snake.steps
                    print('SUCCESS! (steps: {})'.format(self.__snake.steps))
                    break
                if self.__snake.dead or self.__snake.steps > steps_limit:
                    print('FAIL! (steps:{})'.format(self.__snake.steps))
                    if self.__snake.steps > steps_limit:
                        # We call the __write_logs() method because __game_main only writes logs for batch episodes
                        # if the game has ended. In our case, it hasn't technically ended,
                        # but has instead timed out. Therefore, we must manually call the __write_logs() method.
                        self.__write_logs()
                    break
            self.__reset()
            # Resets the map and the snake.
            # Remember, the reset method for the snake draws upon the init_direc,init_bodies, and init_types again,
            # so we can simulate another run.
        suc_ratio = tot_suc / (self.__episode - 1)  # Calculate the number of successes.
        # We subtract one from the episodes because each reset increments self.__episodes.
        # However, the last reset didn't actually start a new episode, so we decrement it.
        avg_suc_steps = 0
        if tot_suc:
            # We make sure that there were successes before calculating the average number of steps needed to succeed.
            avg_suc_steps = tot_suc_steps / tot_suc
        print('\n[Summary]\n'
              'Total: {}\n'
              'Successful: {}\n'
              'Success Ratio: {:.2f}%\n'
              'Average Success Steps:{:.2f}'.format(self.__episode - 1,
                                                    tot_suc,
                                                    100 * suc_ratio,
                                                    avg_suc_steps))
        self.__on_exit()  # Closes the log file. Now the program is done and will exit.

    @staticmethod
    def __get_positive_integer(question):
        """
        This method gets a positive integer from the user.
        This is done by attempting to convert the input to an integer using a try-except block.
        Upon successfully converting the input into an integer, it is then double-checked to see if it is positive.
        :param question: The question to ask when getting the input.
        :return: A positive integer.
        """
        while True:
            try:
                ui = int(input(question))
                # Step 1. Get an input from the user and attempt to convert that into an integer.
                # If conversion is successful, move to Step 2. Otherwise, move to Step 3.
                if ui <= 0:
                    # Step 2: Check if the integer is positive.
                    # If it is not positive, then ask for the input again.
                    # Else, return the integer.
                    print('Sorry. Please input a positive integer.')
                    continue
                return ui
            except ValueError:  # Step 3: Catch the ValueError, and inform the user to enter a valid number.
                print('Please input a valid number.')

    def __game_main(self):
        """
        The main game loop. This is called by self.__batch_episodes when gui is disabled,
        and by the game window when gui is enabled.
        1. If the snake just ate food, then a new piece of food is created.
        2. If the game has ended (which means that the snake has either run into itself or has won),
        then don't do anything.
        3. If AI is enabled, then update the next snake direction, according to what the solver says.
        4. If the GUI has been enabled and the snake is going to move somewhere,
        or if picture logging has been enabled, then write logs.
        5. Move the snake according to next_direc.
        Of course, if next_direc is NONE or Direc.None, the method returns, and so the snake does not move.
        6. Finally, if the snake just won, which means that step 2 has not been triggered yet, then log the results.
        :return: None.
        """
        if not self.__map.has_food():
            self.__map.create_rand_food()
        if self.__pause or self.__episode_end():
            return
        if self.__conf.enable_AI:
            self.__update_direc(self.__solver.next_direc())
        if (self.__conf.show_gui and self.__snake.direc_next != Direc.NONE) or self.__conf.picture_logging:
            self.__write_logs()
        self.__snake.move()
        if self.__episode_end():
            self.__write_logs()

    def __update_direc(self, new_direc):
        """
        This method is triggered by the game main, but more importantly, by key-bindings.
        It checks if the snake is not moving in the opposite direction.
        If it isn't, then it sets the new direction to whatever the parameter is.
        Because next_direc is never deleted by the Snake object,
        it continuously moves in the specified direction until it dies or the direction is changed.
        :param new_direc: A direction for the snake to go to, of type Direc.
        :return: None.
        """
        if Direc.opposite(new_direc) != self.__snake.direc:
            self.__snake.direc_next = new_direc
            if self.__pause:
                # If it's paused, then we still forcibly move the snake once.
                # This can be used to make very precise moves.
                self.__snake.move()

    def __toggle_pause(self):
        """
        Toggles the pause property. This is activated by the key binding <Space>.
        :return: None
        """
        self.__pause = not self.__pause

    def __episode_end(self):
        """
        Checks if the episode has ended.
        This method checks if either the snake is dead (It has lost) or if the snake has won.
        :return: Boolean Value, which depends on whether or not the game has won.
        """
        return self.__snake.dead or self.__map.is_full()

    def __reset(self):
        """
        Resets the snake and increments the episode count.
        :return: None.
        """
        self.__snake.reset()
        self.__episode += 1

    def __on_exit(self):
        """
        Closes the log file if possible. This is called by the gui's on_destroy method and the batch_episode method.
        :return: None.
        """
        if self.__log_file:
            self.__log_file.close()

    def __init_log_file(self):
        """
        Tries to create a logs folder. If it already exists, that's fine,
        but if some weird error occurs, then raise that error and terminate the program.

        Then, tries to open the log file to write to it. If no file exists, that's fine, just don't write to it.
        :return: None.
        """
        try:
            os.makedirs('logs')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            self.__log_file = None
            self.__log_file = open('logs/snake.log', 'w')
        except FileNotFoundError:
            if self.__log_file:
                self.__log_file.close()

    def __write_logs(self):
        """
        Writes game states to log.
        If picture logging is enabled, then an ascii rendering of the game state will be logged at each step.
        :return: None.
        """
        if self.__conf.picture_logging:
            self.__log_file.write('[Episode {} Step {}]\n'.format(self.__episode, self.__snake.steps))
            for i in range(self.__map.num_rows):
                for j in range(self.__map.num_cols):
                    pos = Pos(i, j)
                    t = self.__map.point(pos).type
                    if t == PointType.EMPTY:
                        self.__log_file.write("  ")
                    elif t == PointType.WALL:
                        self.__log_file.write("# ")
                    elif t == PointType.FOOD:
                        self.__log_file.write("F ")
                    elif t == PointType.HEAD_L or t == PointType.HEAD_U or \
                            t == PointType.HEAD_R or t == PointType.HEAD_D:
                        self.__log_file.write("H ")
                    elif pos == self.__snake.tail():
                        self.__log_file.write("T ")
                    else:
                        self.__log_file.write("B ")
                self.__log_file.write("\n")
        self.__log_file.write("[ last/next direction: {}/{} ]\n".format
                              (self.__snake.direc, self.__snake.direc_next))
        self.__log_file.write("\n")
