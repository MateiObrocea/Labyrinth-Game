from pygame import image, transform


class Star:
    """
    Displays star which change the opacity factor if they get collected
    When all the stars are collected the game is won
    """

    def __init__(self, x, y, size):
        self.star_image = image.load("helpers/Images/star.png")
        self.position_x = x
        self.position_y = y
        self.size = (size[0], size[1])
        self.is_collected = False
        self.alpha = 255  # the opacity factor

    def render(self, surface):
        star_image = transform.scale(self.star_image, (50, 50))
        self.star_image.set_alpha(self.alpha)
        surface.blit(star_image, (self.position_x * self.size[0], self.position_y * self.size[1]))

    def collision(self, other_x, other_y):
        # checks if they player is on the star position
        if self.position_x == other_x and self.position_y == other_y:
            return True

    def get_collected(self, other_x, other_y):
        # triggers the collection as soon as the player steps on a star
        if self.collision(other_x, other_y):
            self.alpha = 127
            self.is_collected = True


