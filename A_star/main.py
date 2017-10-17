from queue import PriorityQueue, Queue
from PIL import Image, ImageDraw
from renderboard import BoardRender
import time
import os


class Board:
    def __init__(self, board_name):
        self.start = None
        self.goal = None  # me-irl
        self.board = board_name
        self.board_array = []
        self.read_board()
        self.board_w = len(self.board_array[0])
        self.board_h = len(self.board_array)

    # Returns if a given node is a wall (used by neighbour function)
    def is_wall(self, node):
        x, y = node
        return self.board_array[y][x] == '#'

    # Finds every valid neighbour of a node
    def get_neighbors(self, node):
        x, y = node
        l, t, r, b = (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)
        valid_nodes = []
        for node in [l, t, r, b]:
            x, y = node
            if 0 <= x < self.board_w and 0 <= y < self.board_h and not self.is_wall(node):
                valid_nodes.append(node)
        return valid_nodes

    # Contains the costs of the different terrains
    def cost_node(self, x):
        return {
            'w': 100,   # Water
            'm': 50,    # Mountain
            'f': 10,    # Forest
            'g': 5,     # Grass
            'r': 1,     # Road
        }.get(x, 1)     # Default

    # Finds the cost of a node
    def cost(self, node):
        x, y = node
        return self.cost_node(self.board_array[y][x])

    # Reads the board from the provided files, and makes them a 2d array
    def read_board(self):
        f = open(self.board)
        board = []
        for line in f:
            board.append([c for c in line if c != '\n'])
        # detect start and goal
        for x in range(len(board[0])):
            for y in range(len(board)):
                c = board[y][x]
                if not self.start and c == 'A':
                    self.start = x, y
                if not self.goal and c == 'B':
                    self.goal = x, y

        self.board_array = board
        #  print("Read board of size " + str(len(self.board_array)) +
              #  "," + str(len(self.board_array[0])))

    # Saves the board as a image file
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


# Heuristic used by astar algo
def heuristic(goal, curr):
    # Manhattan distance to goal
    x_diff = abs(curr[0] - goal[0])
    y_diff = abs(curr[1] - goal[1])
    return x_diff + y_diff


#  This astar algorithm is based on the algorithm found at redblobgames.com
def shortest_path(board_name, use_heuristic=False):
    board = Board(board_name)
    start = board.start
    goal = board.goal
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    open_nodes = []
    closed_nodes = []

    # While there are more nodes on the frontier
    while not frontier.empty():
        # Gets the node with the highest priority
        current = frontier.get()[1]
        closed_nodes.append(current)
        # If it has found the goal, it's done!
        if current == goal:
            break

        neighbors = board.get_neighbors(current)
        #  Neighbours named friend for friendliness
        for friend in neighbors:
            #  Calculates the cost of the neighbour based on the weights
            new_cost = cost_so_far[current] + board.cost(friend)
            #  Adds the neighbour to the frontier if it has lower cost than before
            if friend not in cost_so_far or new_cost < cost_so_far[friend]:
                # Adds the neighbour to the open_nodes nodes (for visualization)
                cost_so_far[friend] = new_cost
                # Calculates priority and adds it to queue
                priority = new_cost  # dijkstra
                if use_heuristic:  # a_star
                    priority = new_cost + heuristic(goal, friend)
                frontier.put((priority, friend))
                open_nodes.append(friend)
                # Sets predecessor
                came_from[friend] = current

    for node in closed_nodes:
        if node in open_nodes:
            open_nodes.remove(node)

    print('finished running algorithm!')

    find_path(start, goal, came_from, open_nodes, closed_nodes, board)


def a_star(board_name):
    shortest_path(board_name, use_heuristic=True)


# Same as the astar without the heuristic
def dijkstra(board_name):
    shortest_path(board_name)


def bfs(board_name):
    board = Board(board_name)
    start = board.start
    goal = board.goal
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    open_nodes = []
    closed_nodes = []

    while not frontier.empty():
        current = frontier.get()
        closed_nodes.append(current)
        if current == goal:
            break

        neighbors = board.get_neighbors(current)
        for friend in neighbors:
            if friend not in came_from:
                open_nodes.append(friend)
                frontier.put(friend)
                came_from[friend] = current

    for node in closed_nodes:
        if node in open_nodes:
            open_nodes.remove(node)

    find_path(start, goal, came_from, open_nodes, closed_nodes, board)


# The function that finds the path by iterating through predecessors.
def find_path(start, goal, came_from, open_nodes, closed_nodes, board):
    current = goal
    path = [current]
    # Finds the path by iterating through predecessors to start
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    renderBoard = BoardRender(board.board_array)
    # Renders every closed node
    print("# closed nodes: ", end=' ')
    print(len(closed_nodes))
    for c in closed_nodes:
        x, y = c
        renderBoard.closed(y, x)
    renderBoard.redraw()
    # Renders every open node
    print("# open nodes: ", end=' ')
    print(len(open_nodes))
    for c in open_nodes:
        x, y = c
        renderBoard.considered(y, x)
    renderBoard.redraw()
    # Renders the path
    print("# path: ", end=' ')
    print(len(path))
    for p in path:
        x, y = p
        renderBoard.visited(y, x)
    renderBoard.redraw()

    renderBoard.mainloop()
    time.sleep(1)


if __name__ == "__main__":
    def iterate_path(path, algorithm, board_name=None):
        for board in os.listdir(path):
            board_path = os.path.join(path, board)
            if os.path.isfile(board_path):
                if board_name:
                    if board_name in board_path:
                        algorithm(board_path)
                        continue
                if not board_name:
                    algorithm(board_path)

    iterate_path('trondheim', a_star)
    #  iterate_path('trondheim', dijkstra)
    #  iterate_path('trondheim', bfs)
    #  iterate_path('boards', a_star)
    #  iterate_path('boards', dijkstra)
    #  iterate_path('boards', bfs)
