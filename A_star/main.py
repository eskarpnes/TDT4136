from queue import PriorityQueue
from PIL import Image, ImageDraw
from renderboard import BoardRender


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
        print("start: " + str(self.start))
        print("end: " + str(self.goal))

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


def heuristic(goal, curr):
    #Manhattan distance to goal
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])


def a_star_red_blob(board_name):
    board = Board(board_name)
    start = board.start
    goal = board.goal
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        print(current)

        if current == goal:
            break

        for next in board.get_neighbors(current):
            new_cost = cost_so_far[current] + board.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current


if __name__ == "__main__":
    board = Board("1-1")
