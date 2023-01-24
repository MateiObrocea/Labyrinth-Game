import random
from exercise.grid_element import GridElement


class Maze:
    """
        Generates a grid based maze
        Manages the GreedElements class
        Sets the legal paths of the game
        """

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.grid_size = (grid_size_x, grid_size_y)
        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []
        for x in range(grid_size_x):
            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        self.start = self.grid[0][0]
        self.target = self.grid[-1][-1]
        self.reset_all()

    """
    Resets the GridElements of the maze
    """

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)
        return None

    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.reset_state()


    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                element.draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    def generate_open_maze(self):
        self.reset_all()
        for col in self.grid:
            for cell in col:
                cell.neighbours = self.possible_neighbours(cell)

    def generate_obstacles(self):
        """Generate a Manhattan like grid, with a few road blocks"""

        self.reset_all()
        self.generate_open_maze()

        # The basic boxes
        for n in range(1, self.grid_size[1], 5):
            for m in range(1, self.grid_size[0], 5):
                max_x = min(3, self.grid_size[0] - m - 1)
                max_y = min(3, self.grid_size[1] - n - 1)
                for x in range(0, max_x):
                    self.del_link(self.grid[m + x][n], self.grid[m + x][n - 1])
                    self.del_link(self.grid[m + x][n + max_y], self.grid[m + x][n + max_y - 1])
                for y in range(0, max_y):
                    self.del_link(self.grid[m][n + y], self.grid[m - 1][n + y])
                    self.del_link(self.grid[m + max_x][n + y], self.grid[m + +max_x - 1][n + y])

        # add a few random gaps
        for i in range(max(self.grid_size)):
            random_row = random.choice(self.grid)
            random_element = random.choice(random_row)
            possible = self.possible_neighbours(random_element)
            for cell in possible[:]:
                if cell in random_element.get_neighbours():
                    possible.remove(cell)
            if len(possible) > 0:
                random_neighbor = random.choice(possible)
                self.add_link(random_element, random_neighbor)

        # vertical roadblocks
        block_x = random.choice(range(5, self.grid_size[0], 5))
        self.del_link(self.grid[block_x][0], self.grid[block_x - 1][0])
        for m in range(4, self.grid_size[1] - 2, 5):
            block_x = random.choice(range(3, self.grid_size[0], 5))
            self.del_link(self.grid[block_x][m], self.grid[block_x - 1][m])
            self.del_link(self.grid[block_x][m + 1], self.grid[block_x - 1][m + 1])
        block_x = random.choice(range(3, self.grid_size[0], 5))
        self.del_link(self.grid[block_x][self.grid_size[1] - 1], self.grid[block_x - 1][self.grid_size[1] - 1])

        # horizontal roadblocks
        block_y = random.choice(range(3, self.grid_size[1], 5))
        self.del_link(self.grid[0][block_y], self.grid[0][block_y - 1])
        for n in range(4, self.grid_size[0] - 2, 5):
            block_y = random.choice(range(3, self.grid_size[1], 5))
            self.del_link(self.grid[n][block_y], self.grid[n][block_y - 1])
            self.del_link(self.grid[n + 1][block_y], self.grid[n + 1][block_y - 1])
        block_y = random.choice(range(3, self.grid_size[1], 5))
        self.del_link(self.grid[self.grid_size[0] - 1][block_y], self.grid[self.grid_size[0] - 1][block_y - 1])
