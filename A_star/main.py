from PIL import Image, ImageDraw
from renderboard import BoardRender
from heapq import heappush, heappop


class Board:
    def __init__(self, board_name):
        self.start = None
        self.goal = None  # me-irl
        self.board = "boards/board-" + board_name + ".txt"
        self.board_array = []
        self.read_board()
        self.renderedBoard = BoardRender(self.board_array)

    def read_board(self):
        f = open(self.board)
        board = []
        for line in f:
            board.append([c for c in line if c != '\n'])
        print(board)
        for x in range(len(board[0])):
            for y in range(len(board)):
                c = board[y][x]
                if c == '\n':
                    pass
                if not self.start and c == 'A':
                    self.start = x, y
                if not self.goal and c == 'B':
                    self.goal = x, y

        self.board_array = board
        print("Read board of size " + str(len(self.board_array)) +
              "," + str(len(self.board_array[0])))

    def save_image_board(self):
        img = Image.new(
            'RGB', (len(self.board_array[0]) * 20,
                    len(self.board_array) * 20), "white")
        idraw = ImageDraw.Draw(img)
        for x in range(len(self.board_array[0])):
            for y in range(len(self.board_array)):
                color = self.colors[self.board_array[y][x]]
                idraw.rectangle(
                    [x * 20, y * 20, x * 20 + 20, y * 20 + 20], color)
        img.show()


inf = float("inf")


def heuristic(a, b):
    # Manhattan distance to goal
    return abs(a.x - b.x) + abs(a.y - b.y)


if __name__ == "__main__":
    board = Board("1-1")
