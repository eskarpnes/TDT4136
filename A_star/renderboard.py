import tkinter as tk


def rgb(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


colors = {
    'w': rgb(73, 216, 245),  # Water
    'm': rgb(99, 99, 99),  # Mountain
    'f': rgb(3, 82, 0),  # Forest
    'g': rgb(50, 200, 50),  # Grass
    'r': rgb(114, 80, 41),  # Road
    '.': rgb(255, 255, 255),  # Nothing
    '#': rgb(114, 114, 114),  # Wall
    'A': rgb(90, 180, 90),  # Start
    'B': rgb(255, 90, 90),  # End
    'v': rgb(255, 0, 0),
    'c': rgb(150, 150, 150)
}


def get_color(c):
    # c: 'w' for water, '.' for nothing, etc.
    return colors.get(c)


class BoardRender(tk.Tk):
    def __init__(self, board_array):
        board_x = len(board_array[0])
        board_y = len(board_array)
        tk.Tk.__init__(self)
        self.cell_size = 15
        self.canvas = tk.Canvas(
            self,
            width=self.cell_size * board_x,  # board width * square size
            height=self.cell_size * board_y,  # board width * square size
            borderwidth=0,
            highlightthickness=0,
            relief='flat')
        self.canvas.pack(side="top", fill="both", expand="true")

        self.rect = {}
        self.oval = {}
        for column in range(board_x):
            for row in range(board_y):
                x1 = column * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.rect[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, tags="rect")
                self.oval[row, column] = self.canvas.create_oval(
                    x1 + 4, y1 + 4, x2 - 4, y2 - 4, tags="oval")

        self.canvas.itemconfig("rect", fill="")
        self.canvas.itemconfig("oval", fill="", outline="")

        for i in range(board_y):
            for j in range(board_x):
                self.fill_square(j, i, color=board_array[i][j])

    def fill_square(self, x, y, color):
        #  self.canvas.itemconfig("rect", fill=get_color(color))
        pos = self.rect[y, x]
        self.canvas.itemconfig(pos, fill=get_color(color))

    def redraw(self):
        self.update_idletasks()
        self.update()

    def visited(self, x, y):
        pos = self.oval[x, y]
        self.canvas.itemconfig(pos, fill=get_color('v'))

    def considered(self, x, y):
        pos = self.oval[x, y]
        self.canvas.itemconfig(pos, fill=get_color('c'))
