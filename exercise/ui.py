from pygame import image


class UI:

    def __init__(self):
        self.pentagram = image.load("helpers/Images/8-bit_pentagram.png")

    def render_end(self, surface, x, y):
        surface.blit(self.pentagram, (x, y))
