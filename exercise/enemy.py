from agent import Agent
from exercise.search import Search
from pygame import image


class Enemy(Agent):

    def __init__(self, x, y, size, maze):
        super().__init__(x, y, size)
        self.search = Search(maze)
        self.sprites = []
        for i in range(4):
            self.sprites.append(image.load(f"helpers/Images/kot_{i+1}.png"))
        self.sprite_animation_speed = 1000

    def move(self, direction):

        path = self.search.get_path()
        if path:
            self.sprite_animation_speed = 6
            for node in path:
                self.position_x = node[0]
                self.position_y = node[1]
        else:
            self.sprite_animation_speed = 1000

    def seek_player(self):
        self.search.a_star_search()



