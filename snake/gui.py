# coding=utf-8
""" Definitions for the game window."""
import tkinter as tk
from snake.map import Pos, PointType


class GameWindow(tk.Tk):
    """
    This is the game window. It's what you see.
    """

    def __init__(self, config, m, title, snake=None, on_exit=None, keybindings=None):
        super().__init__()
        super().title(title)
        super().resizable(width=False, height=False)
        super().configure(background=config.colour_bg)
        if config.show_info_panel:
            super().geometry('{}x{}'.format(config.window_width, config.window_height))
        self.__conf = config
        self.__map = m
        self.__snake = snake
        self.__grid_width = config.map_width / (m.num_rows - 2)
        self.__grid_height = config.map_height / (m.num_cols - 2)
        self.__init_widgets()
        self.__init_draw_params()

        def on_destroy():
            """

            :return:
            """
            if callable(on_exit):
                on_exit()
            self.destroy()

        self.__init_keybindings(keybindings, on_destroy)

    def show(self, game_loop=None):
        """

        :param game_loop:
        :return:
        """

        def cb():
            """

            :return: Void.
            """
            if callable(game_loop):
                game_loop()
            self.__update_contents()
            self.after(self.__conf.interval_draw, cb)

        self.after(100, cb)
        self.mainloop()

    def __init_widgets(self):
        self.__canvas = tk.Canvas(
                self,
                bg=self.__conf.colour_bg,
                width=self.__conf.map_width,
                height=self.__conf.map_height,
                highlightthickness=0
        )
        self.__canvas.pack(side=tk.LEFT)
        if self.__conf.show_info_panel:
            frm = tk.Frame(
                    self,
                    bg=self.__conf.colour_bg
            )
            frm.pack(side=tk.RIGHT, anchor=tk.N)
            self.__info_var = tk.StringVar()
            tk.Message(
                    frm,
                    textvariable=self.__info_var,
                    fg=self.__conf.colour_txt,
                    bg=self.__conf.colour_bg,
                    font=self.__conf.font_info
            ).pack(side=tk.TOP, anchor=tk.W)
            scale = tk.Scale(
                    frm,
                    font=self.__conf.font_info,
                    fg=self.__conf.colour_txt,
                    bg=self.__conf.colour_bg,
                    highlightthickness=0,
                    from_=0,
                    to=self.__conf.interval_draw_max,
                    orient=tk.HORIZONTAL,
                    length=self.__conf.window_width - self.__conf.map_width,
                    showvalue=False,
                    tickinterval=0,
                    resolution=1,
                    command=self.__update_speed
            )
            scale.pack(side=tk.TOP, anchor=tk.W)
            scale.set(self.__conf.interval_draw)

    def __update_speed(self, speed):
        self.__conf.interval_draw = int(speed)

    def __init_keybindings(self, keybindings, ondestroy):
        self.bind('<Escape>', lambda e: ondestroy())
        self.protocol('WM_DELETE_WINDOW', ondestroy)
        if keybindings:
            for kb in keybindings:
                self.bind(kb[0], kb[1])

    def __init_draw_params(self):
        pad_ratio = self.__conf.grid_pad_ratio  # Easier way to reference the pad ratio. Less verbose.
        food_pad_ratio = 0.9 * pad_ratio  # Food is a little larger than the normal pad ratio.
        self.__dx1 = pad_ratio * self.__grid_width  # Left side padding
        self.__dx2 = (1 - pad_ratio) * self.__grid_width  # Right side padding
        self.__dy1 = pad_ratio * self.__grid_height  # Top side padding
        self.__dy2 = (1 - pad_ratio) * self.__grid_height  # Bottom side padding
        self.__dx1_food = food_pad_ratio * self.__grid_width  # Same thing as above,
        self.__dx2_food = (1 - food_pad_ratio) * self.__grid_width  # But for food, since food is a little larger
        self.__dy1_food = food_pad_ratio * self.__grid_height
        self.__dy2_food = (1 - food_pad_ratio) * self.__grid_height

    def __update_contents(self):
        """
        The main function for drawing the ui. Remember, all of these changes happen inside the buffer until updated.
        1. Clear the window.
        2. Draw the background: A black rectangle.
        3. Draw grid-lines, if enabled.
        4. Draw the info panel, if enabled.
        5. Draw map contents, aka the snake and food.
        6. Update the window to show the new contents.
        :return:
        """
        self.__canvas.delete(tk.ALL)
        self.__draw_bg()
        if self.__conf.show_grid_line:
            self.__draw_grid_line()
        if self.__conf.show_info_panel:
            self.__draw_info_panel()
        self.__draw_map_contents()
        self.update()

    def __draw_bg(self):
        self.__canvas.create_rectangle(0,
                                       0,
                                       self.__conf.map_width,
                                       self.__conf.map_height,
                                       fill=self.__conf.colour_bg,
                                       outline='')

    def __draw_grid_line(self):
        for i in range(1, self.__map.num_rows - 2):
            for j in range(1, self.__map.num_cols - 2):
                x = i * self.__grid_width
                y = j * self.__grid_height
                # Vertical Line
                self.__canvas.create_line(x, 0, x, self.__conf.map_height,
                                          fill=self.__conf.colour_line)
                # Horizontal Line
                self.__canvas.create_line(0, y, self.__conf.map_width, y,
                                          fill=self.__conf.colour_line)

    def __draw_info_panel(self):
        self.__canvas.create_line(self.__conf.map_width - 1,
                                  0,
                                  self.__conf.map_width - 1,
                                  self.__conf.map_height,
                                  fill=self.__conf.colour_line)
        if self.__snake.dead:
            status_str = self.__conf.info_status[1]
        elif self.__map.is_full():
            status_str = self.__conf.info_status[2]
        else:
            status_str = self.__conf.info_status[0]

        self.__info_var.set(self.__conf.info_str % (
            self.__conf.solver_name[:-6].lower(),
            status_str,
            self.__snake.steps,
            self.__snake.len(),
            self.__map.capacity))

    def __draw_map_contents(self):
        for i in range(self.__map.num_rows - 2):
            for j in range(self.__map.num_cols - 2):
                self.__draw_grid(j * self.__grid_width,
                                 i * self.__grid_width,
                                 self.__map.point(Pos(i + 1, j + 1)).type
                                 )

    def __draw_grid(self, x, y, t):
        """
        Draws a single point on the grid, whether it be a snake body, a wall, or a piece of food.
        :param x: An integer denoting the location, in pixels of the left side of the grid cell.
        :param y: An integer denoting the location, in pixels, of the top side of the grid cell.
        :param t: The point type of the cell of class PointType, which is an enum.
        :return: None.
        """
        if t == PointType.WALL:
            self.__canvas.create_rectangle(x, y,
                                           x + self.__grid_width, y + self.__grid_height,
                                           fill=self.__conf.colour_wall, outline='')
        elif t == PointType.FOOD:
            self.__canvas.create_rectangle(x + self.__dx1_food, y + self.__dy1_food,
                                           x + self.__dx2_food, y + self.__dy2_food,
                                           fill=self.__conf.colour_food, outline='')
        elif t == PointType.HEAD_L:
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__grid_width, y + self.__dy2,
                                           fill=self.__conf.colour_head, outline='')
        elif t == PointType.HEAD_U:
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__dx2, y + self.__grid_height,
                                           fill=self.__conf.colour_head, outline='')
        elif t == PointType.HEAD_R:
            self.__canvas.create_rectangle(x, y + self.__dy1,
                                           x + self.__dx2, y + self.__dy2,
                                           fill=self.__conf.colour_head, outline='')
        elif t == PointType.HEAD_D:
            self.__canvas.create_rectangle(x + self.__dx1, y,
                                           x + self.__dx2, y + self.__dy2,
                                           fill=self.__conf.colour_head, outline='')
        elif t == PointType.BODY_LU:
            self.__canvas.create_rectangle(x, y + self.__dy1,
                                           x + self.__dx1, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
            self.__canvas.create_rectangle(x + self.__dx1, y,
                                           x + self.__dx2, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
        elif t == PointType.BODY_UR:
            self.__canvas.create_rectangle(x + self.__dx1, y,
                                           x + self.__dx2, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__grid_width, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
        elif t == PointType.BODY_RD:
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__grid_width, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__dx2, y + self.__grid_height,
                                           fill=self.__conf.colour_body, outline='')
        elif t == PointType.BODY_DL:
            self.__canvas.create_rectangle(x + self.__dx1, y + self.__dy1,
                                           x + self.__dx2, y + self.__grid_height,
                                           fill=self.__conf.colour_body, outline='')
            self.__canvas.create_rectangle(x, y + self.__dy1,
                                           x + self.__dx1, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
        elif t == PointType.BODY_HOR:
            self.__canvas.create_rectangle(x, y + self.__dy1,
                                           x + self.__grid_width, y + self.__dy2,
                                           fill=self.__conf.colour_body, outline='')
        elif t == PointType.BODY_VER:
            self.__canvas.create_rectangle(x + self.__dx1, y,
                                           x + self.__dx2, y + self.__grid_height,
                                           fill=self.__conf.colour_body, outline='')
