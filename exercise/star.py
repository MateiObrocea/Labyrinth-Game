from pygame import draw


class Star:

    def __init__(self, x, y, size):
        self.position_x = x
        self.position_y = y
        self.size = (size[0], size[1])
        self.star_color = (255, 255, 0)
        self.is_collected = False

    def render(self, surface):
        draw.rect(surface, self.star_color,
                  (self.position_x * self.size[0] + 4, self.position_y * self.size[1] + 4, self.size[0] - 8, self.size[1] - 8), 0)
        # draw.rect(surface, (255, 255, 255),
        #           (100, 100, 20, 20), 0)

    def collision(self, other_x, other_y):
        if self.position_x == other_x and self.position_y == other_y:
            return True

    def get_collected(self, other_x, other_y):
        # print(self.star_color)
        if self.collision(other_x, other_y):
            self.star_color = (0, 0, 0)
            self.is_collected = True


