import pygame


class Agent:
    """
    Super class for the players and the enemy
    Defines walker on the board
    """

    def __init__(self, x, y, size):
        self.position_x = x
        self.position_y = y
        self.size = (size[0], size[1])
        self.counter = 0
        self.sprites = []
        self.sprite_animation_speed = 0
        self.previous_x = x
        self.previous_y = y
        self.angle = 0

    """
    Method which cycles through the sprites of the agent, generating a gif
    A similar case is in UI clas for the scratch animation
    """

    def draw_sprite(self, surface):
        self.counter += 1
        self.angle = self.calculate_direction()
        if self.counter >= len(self.sprites) * self.sprite_animation_speed:
            self.counter = 0
        sprite = pygame.transform.scale(self.sprites[self.counter // self.sprite_animation_speed], (50, 50))
        sprite = pygame.transform.rotate(sprite, self.angle) # rotates according to the direction of the movement
        surface.blit(sprite, (self.position_x * self.size[0],  self.position_y * self.size[1]))

    """
    Computes the direction towards which the sprites move
    """
    def calculate_direction(self):
        if self.previous_x < self.position_x:
            self.previous_x = self.position_x
            return 270
        if self.previous_x > self.position_x:
            self.previous_x = self.position_x
            return 90
        if self.previous_y < self.position_y:
            self.previous_y = self.position_y
            return 180
        if self.previous_y > self.position_y:
            self.previous_y = self.position_y
            return 0
        return self.angle


    def move(self, direction):
        pass # will be overwritten in the subclasses
