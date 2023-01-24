from agent import Agent
from pygame import image


class Player(Agent):

    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.sprites = []
        for i in range(4):
            self.sprites.append(image.load(f"helpers/Images/bird_{i+1}.png"))
        self.sprite_animation_speed = 4

    def move(self, direction):
        if direction == 0:
            self.position_y = self.position_y - 1
        if direction == 1:
            self.position_x = self.position_x + 1
        if direction == 2:
            self.position_y = self.position_y + 1
        if direction == 3:
            self.position_x = self.position_x - 1