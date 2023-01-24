from pygame import image, time


class UI:

    def __init__(self):
        self.pentagram = image.load("helpers/Images/8-bit_pentagram.png")
        self.dead_cat = image.load("helpers/Images/dead_kot.png")
        self.scratch_images = []
        for i in range(3):
            self.scratch_images.append((image.load(f"helpers/Images/cat_scratch_{i + 1}.png")))
        self.messages = [image.load("helpers/Images/game_over.png"),
                         image.load("helpers/Images/you_win.png")]
        self.counter = 0
        self.counter_2 = 0
        self.win_animation_speed = 3
        self.lose_animation_speed = 3
        self.end_game = False

    def render_game_over(self, surface, x, y, condition):
        if condition:
            self.counter += 1
            if self.counter >= len(self.scratch_images) * self.win_animation_speed:
                self.counter = 0
            surface.blit(self.scratch_images[self.counter // self.win_animation_speed],
                         (x, y))
            surface.blit(self.messages[0], (x + 150, y + 500))
            self.counter_2 += 1
            if self.counter_2 > self.win_animation_speed * 2:
                time.delay(2000)
                self.end_game = True

    def render_you_win(self, surface, x, y, condition):
        if condition:
            self.counter += 1
            self.counter_2 += 1
            if self.counter <= 20:
                surface.blit(self.pentagram, (x, y))
            else:
                surface.blit(self.dead_cat, (x - 50, y - 150))
                surface.blit(self.messages[1], (x + 140, y + 350))

            if self.counter_2 > 25:
                time.delay(2000)
                self.end_game = True

    # def render_start_game(self, surface, x, y):
    #     time.delay(2000)
    #     surface.blit(self.pentagram, (x, y))
    #     pass

