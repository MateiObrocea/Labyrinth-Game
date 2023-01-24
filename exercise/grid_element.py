from random import uniform

from pygame import draw


class GridElement:
    """
    GridElement used as a tile in the maze
    """

    def __init__(self, x, y, size):
        self.position = (x, y)
        self.neighbours = []
        self.size = (size[0], size[1])
        self.parent = None
        self.distance = None
        self.score = None
        self.init_color = (uniform(25, 100), uniform(135, 205), 0)
        self.wall_color = (120, 80, 0)
        self.set_color(self.init_color)

    """
    Overload the less than operator
    """

    def __lt__(self, other):
        return (self.score is not None) and (other.score is None or self.score < other.score)

    """
    Remove all neighbours
    """

    def reset_neighbours(self):
        pass
        self.neighbours = []

    """
    Sets the state of the GridElement 
    """

    def reset_state(self):
        self.parent = None
        self.score = None
        self.distance = None
        self.set_color(self.init_color)

    def get_neighbours(self):
        return self.neighbours[:]

    """
     Method to calculate the Manhattan distance from a certain 
     GridElement to another GridElement of the exercise
     """

    def manhattan_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return x_distance + y_distance

    def direction(self, other):
        return other.position[0] - self.position[0], other.position[1] - self.position[1]

    def set_score(self, score):
        self.score = score

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    """
    Assign the GridElement used to reach this GridElement
    """

    def set_parent(self, parent):
        self.parent = parent
        if parent.distance is not None:
            self.distance = parent.distance + 1

    def set_color(self, color):
        self.color = color

    def draw_grid_element(self, surface):
        draw.rect(surface, self.color,
                  (self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1]), 0)

        # discard the directions where neighbours are
        compass = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        # The four directions
        for neighbour in self.neighbours:
            if self.direction(neighbour) in compass:
                compass.remove(self.direction(neighbour))

        for direction in compass:
            if direction == (0, -1):  # North
                draw.line(surface, self.wall_color, (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]), 8)
            if direction == (1, 0):  # East
                draw.line(surface, self.wall_color, ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 8)
            if direction == (0, 1):  # South
                draw.line(surface, self.wall_color, (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]),
                          ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 8)
            if direction == (-1, 0):  # West
                draw.line(surface, self.wall_color, (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                          (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]), 8)

        # This draw an arrow to from the parent
        # if self.parent is not None:
        #
        #     vector = self.direction(self.parent)
        #
        #     center = ((self.position[0]+0.5) * self.size[0],(self.position[1]+0.5) * self.size[1])
        #
        #     if vector[0] != 0:
        #         left_point = (center[0]+(vector[0]-vector[1])*self.size[0]/5,center[1]+(vector[1]-vector[0])*self.size[0]/5)
        #         right_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5, center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #     else:
        #         left_point = (center[0] + (vector[0] - vector[1]) * self.size[0] / 5,
        #                       center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #         right_point = (center[0] + (vector[0] + vector[1]) * self.size[0] / 5,
        #                        center[1] + (vector[1] + vector[0]) * self.size[0] / 5)
        #     draw.polygon(surface, (100,100,100),(center,left_point,right_point))
        #     entry_point= (center[0]+vector[0]*self.size[0]/2,center[1]+vector[1]*self.size[1]/2)
        #     end_point = (center[0] + vector[0] * self.size[0] / 5, center[1] + vector[1] * self.size[1] / 5)
        #     draw.line(surface, (100,100,100),end_point,entry_point,int(self.size[0]/20)+1)


