import random


class Board:
    def __init__(self, rows=5, cols=5, obstacle_ratio=0.2):
        if rows < 5 or cols < 5:
            raise ValueError("Plansza musi mieć co najmniej 5x5 pól.")
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.stop = None
        self.obstacles = set()
        self.generate_board(obstacle_ratio)

    def generate_board(self, obstacle_ratio):
        self.place_start_stop()
        self.place_obstacles(obstacle_ratio)

    def place_start_stop(self):
        edges = []
        for i in range(self.rows):
            edges.append((i, 0))
            edges.append((i, self.cols - 1))
        for j in range(1, self.cols - 1):
            edges.append((0, j))
            edges.append((self.rows - 1, j))

        self.start, self.stop = random.sample(edges, 2)
        self.grid[self.start[0]][self.start[1]] = 'A'
        self.grid[self.stop[0]][self.stop[1]] = 'B'

    def place_obstacles(self, obstacle_ratio):
        total_cells = self.rows * self.cols
        obstacle_count = int(total_cells * obstacle_ratio)
        while len(self.obstacles) < obstacle_count:
            cell = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if cell not in self.obstacles and cell != self.start and cell != self.stop:
                self.obstacles.add(cell)
                self.grid[cell[0]][cell[1]] = 'X'

    def is_within_bounds(self, position):
        r, c = position
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_obstacle(self, position):
        return position in self.obstacles

    def display(self, path=None):
        display_grid = [row.copy() for row in self.grid]
        if path:
            for pos in path:
                if pos != self.start and pos != self.stop:
                    display_grid[pos[0]][pos[1]] = '.'
        for row in display_grid:
            print(' '.join(row))

    def export_to_file(self, filename='board.txt', path=None):
        with open(filename, 'w') as f:
            display_grid = [row.copy() for row in self.grid]
            if path:
                for pos in path:
                    if pos != self.start and pos != self.stop:
                        display_grid[pos[0]][pos[1]] = '.'
            for row in display_grid:
                f.write(' '.join(row) + '\n')
