from pygame import image, time


class UI:

    def __init__(self):
        self.pentagram = image.load("helpers/Images/8-bit_pentagram.png")

    def render_end(self, surface, x, y, condition):
        if condition:
            surface.blit(self.pentagram, (x, y))

    def spawn(self, surface, x, y, delay_value, condition):
        if condition:
            # surface.blit(self.pentagram, (x, y))
            # self.render_end(surface, x, y, condition)
            time.delay(delay_value)



