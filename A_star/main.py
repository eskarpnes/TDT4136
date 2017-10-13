from queue import PriorityQueue
from PIL import Image, ImageDraw
from renderboard import BoardRender
import time


class Board:
    def __init__(self, board_name):
        self.start = None
        self.goal = None  # me-irl
        self.board = "boards/board-" + board_name + ".txt"
        self.board_array = []
        self.read_board()
        self.board_w = len(self.board_array[0])
        self.board_h = len(self.board_array)
        #  self.renderedBoard = BoardRender(self.board_array)

    def is_wall(self, node):
        x, y = node
        return self.board_array[y][x] == '#'

    def get_neighbors(self, node):
        # fetch all surrounding neighbors of node
        x, y = node
        l, t, r, b = (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)
        valid_nodes = []
        for node in [l, t, r, b]:
            x, y = node
            if x >= 0 and x < self.board_w:
                if y >= 0 and y < self.board_h:
                    # this is a possible node, check for walls
                    if not self.is_wall(node):
                        valid_nodes.append(node)
        return valid_nodes

    def cost_node(self, x):
        return {
            'w': 100,  # Water
            'm': 50,  # Mountain
            'f': 10,  # Forest
            'g': 5,  # Grass
            'r': 1,  # Road
        }.get(x, 1)  # Default

    def cost(self, node):
        x, y = node
        cost_num = self.cost_node(self.board_array[y][x])
        return cost_num

    def read_board(self):
        f = open(self.board)
        board = []
        for line in f:
            board.append([c for c in line if c != '\n'])
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


def heuristic(goal, curr):
    # Manhattan distance to goal
    x_diff = abs(curr[0] - goal[0])
    y_diff = abs(curr[1] - goal[1])
    return x_diff + y_diff


def a_star_red_blob(board_name):
    board = Board(board_name)
    start = board.start
    goal = board.goal
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    considered = []

    while not frontier.empty():
        current = frontier.get()[1]
        if current == goal:
            break

        neighbors = board.get_neighbors(current)
        for friend in neighbors:
            new_cost = cost_so_far[current] + board.cost(friend)
            if friend not in cost_so_far or new_cost < cost_so_far[friend]:
                considered.append(friend)
                cost_so_far[friend] = new_cost
                priority = new_cost + heuristic(goal, friend)
                frontier.put((priority, friend))
                came_from[friend] = current
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    print([p for p in path])
    renderBoard = BoardRender(board.board_array)
    for c in considered:
        x, y = c
        renderBoard.considered(y, x)
        renderBoard.redraw()
    for p in path:
        x, y = p
        renderBoard.visited(y, x)
        renderBoard.redraw()
        time.sleep(0.05)
    #  renderBoard.mainloop()
    time.sleep(1)


if __name__ == "__main__":
    boards = "1-1 1-2 1-3 1-4 2-1 2-2 2-3 2-4".split()
    for b in boards:
        print(b)
        #  board = Board("1-1")
        a_star_red_blob(b)
