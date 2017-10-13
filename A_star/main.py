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

    def cost(self, current_node, next_node):
        #  curr_x, curr_y = current_node
        #  next_x, next_y = next_node
        return 1

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
    return abs(curr[0] - goal[0]) + abs(curr[1] - goal[1])


def a_star_red_blob(board_name):
    board = Board(board_name)
    start = board.start
    goal = board.goal
    print("Start: " + str(start))
    print("Goal: " + str(goal))
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    path = []

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        neighbors = board.get_neighbors(current)
        for friend in neighbors:
            new_cost = cost_so_far[current] + board.cost(current, friend)
            if friend not in cost_so_far or new_cost < cost_so_far[friend]:
                cost_so_far[friend] = new_cost
                priority = new_cost + heuristic(goal, friend)
                frontier.put(friend, priority)
                came_from[friend] = current
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    print([p for p in path])
    renderBoard = BoardRender(board.board_array)
    for p in path:
        x, y = p
        renderBoard.visited(y, x)
        renderBoard.redraw()
        time.sleep(0.3)
    #  renderBoard.mainloop()
    time.sleep(2)


if __name__ == "__main__":
    boards = "1-1 1-2 1-3 1-4".split()
    for b in boards:
        print(b)
        #  board = Board("1-1")
        a_star_red_blob(b)
