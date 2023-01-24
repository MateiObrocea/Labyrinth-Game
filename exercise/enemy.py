from agent import Agent
from exercise.search import Search
from pygame import image


class Enemy(Agent):
    """
    Subclass of the agent
    Represents the cat which chases the raven
    """
    def __init__(self, x, y, size, maze):
        super().__init__(x, y, size)
        self.search = Search(maze)
        self.sprites = []
        for i in range(4):
            self.sprites.append(image.load(f"helpers/Images/kot_{i+1}.png"))
        self.sprite_animation_speed = 1000 # very slow speed, in case the cat stands still

    """
    The overwritten movement method
    If there is an available path, follow that path
    """

    def move(self, direction):
        path = self.search.get_path()
        if path:
            self.sprite_animation_speed = 6
            for node in path:
                self.position_x = node[0]
                self.position_y = node[1]
        else:
            self.sprite_animation_speed = 1000  # if not available path, don't cycle through the images (pause the gif)

    def seek_player(self):
        self.search.a_star_search()  # computes the path to be followed



