from PIL import Image, ImageDraw
from renderboard import BoardRender
from heapq import heappush, heappop


class Board:
    def __init__(self, board_name):
        self.board = "boards/board-" + board_name + ".txt"
        self.board_array = []
        self.read_board()
        self.renderedBoard = BoardRender(self.board_array)

    def read_board(self):
        f = open(self.board)
        for line in f:
            self.board_array.append([c for c in line if c != '\n'])
        print("Read board of size " + str(len(self.board_array)) +
              "," + str(len(self.board_array[0])))

    def save_image_board(self):
        img = Image.new(
            'RGB', (len(self.board_array[0]) * 20, len(self.board_array) * 20), "white")
        idraw = ImageDraw.Draw(img)
        for x in range(len(self.board_array[0])):
            for y in range(len(self.board_array)):
                color = self.colors[self.board_array[y][x]]
                idraw.rectangle(
                    [x * 20, y * 20, x * 20 + 20, y * 20 + 20], color)
        img.show()


inf = float("inf")


# G - the graph, s - the start node, t - the goal, h - the heuristic formula
def a_star(G, s, t, h):
    P, Q = {}, [(h(s), None, s)]  # Preds and queue w/heuristic
    while Q:  # Still unprocessed nodes?
        d, p, u = heappop(Q)  # Node with lowest heuristic
        if u in P: continue  # Already visited? Skip it
        P[u] = p  # Set path predecessor
        if u == t: return d - h(t), P  # Arrived! Ret. dist and preds
        for v in G[u]:  # Go through all neighbours
            w = G[u][v] - h(u) + h(v)  # Modify weight wrt heuristic
            heappush(Q, (d + w, u, v))  # Add to queue, w/heur as pri
    return inf, None  # Didn't get to t


if __name__ == "__main__":
    board = Board("1-1")
