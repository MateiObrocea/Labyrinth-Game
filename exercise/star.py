from pygame import draw, image, transform


class Star:

    def __init__(self, x, y, size):
        self.star_image = image.load("helpers/Images/star.png")
        self.position_x = x
        self.position_y = y
        self.size = (size[0], size[1])
        self.is_collected = False
        self.alpha = 255

    def render(self, surface):
        star_image = transform.scale(self.star_image, (50, 50))
        self.star_image.set_alpha(self.alpha)
        surface.blit(star_image, (self.position_x * self.size[0], self.position_y * self.size[1]))

    def collision(self, other_x, other_y):
        if self.position_x == other_x and self.position_y == other_y:
            return True

    def get_collected(self, other_x, other_y):
        # print(self.star_color)
        if self.collision(other_x, other_y):
            self.alpha = 127
            self.is_collected = True


