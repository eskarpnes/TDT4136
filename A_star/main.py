from PIL import Image, ImageDraw
import tkinter


class Board:

    def __init__(self):
        self.board_array = []
        self.colors = {
            'w': (73, 216, 245),  # Water
            'm': (99, 99, 99),  # Mountain
            'f': (3, 82, 0),  # Forest
            'g': (50, 200, 50),  # Grass
            'r': (114, 80, 41),  # Road
            '.': (255, 255, 255),  # Nothing
            '#': (114, 114, 114),  # Wall
            'A': (90, 180, 90),  # Start
            'B': (255, 90, 90),  # End
        }

    def read_board(self, board_name):
        f = open("boards/board-" + board_name + ".txt")
        for line in f:
            self.board_array.append([c for c in line if c != '\n'])

    def save_image_board(self):
        img = Image.new('RGB', (len(self.board_array[0]) * 20, len(self.board_array) * 20), "white")
        idraw = ImageDraw.Draw(img)
        for x in range(len(self.board_array[0])):
            for y in range(len(self.board_array)):
                color = self.colors[self.board_array[y][x]]
                idraw.rectangle([x*20, y*20, x*20+20, y*20+20], color)
        img.show()

    def render_board(self):
        for x in range(len(self.board_array[0])):
            for y in range(len(self.board_array)):


class Astar:
    pass


if __name__ == "__main__":
    board = Board()
    board.read_board("1-1")
    board.render_board()
