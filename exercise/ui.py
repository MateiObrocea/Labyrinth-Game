from pygame import image, time, mixer


class UI:
    """
    class for user interface, which displays win and lose messages, when it is the case
    """

    def __init__(self):
        self.pentagram = image.load("helpers/Images/8-bit_pentagram.png")
        self.dead_cat = image.load("helpers/Images/dead_kot.png")
        self.scratch_images = []
        for i in range(3):
            self.scratch_images.append((image.load(f"helpers/Images/cat_scratch_{i + 1}.png")))

        self.messages = [image.load("helpers/Images/game_over.png"),
                         image.load("helpers/Images/you_win.png")]

        self.meow = mixer.Sound("helpers/Audio/angry_meow.mp3")
        self.meow.set_volume(0.5)

        self.lose_sound = mixer.Sound("helpers/Audio/lose_sound.mp3")
        self.lose_sound.set_volume(0.5)

        self.background_song = mixer.Sound("helpers/Audio/8_bit_background.mp3")
        self.background_song.set_volume(0.4)
        self.background_song.play(10)

        self.counter = 0  # help with the animation
        self.counter_2 = 0  # help with the animation
        self.win_animation_speed = 3
        self.lose_animation_speed = 3
        self.end_game = False

    def render_game_over(self, surface, x, y, condition):
        if condition:
            self.counter += 1

            # cycles through the array of scratch images
            if self.counter >= len(self.scratch_images) * self.lose_animation_speed:
                self.counter = 0
            surface.blit(self.scratch_images[self.counter // self.lose_animation_speed],
                         (x, y))
            surface.blit(self.messages[0], (x + 150, y + 500))
            self.counter_2 += 1
            if self.counter_2 > self.win_animation_speed * 2:

                # after a certain threshold the animation stops and the program exits
                self.background_song.stop()
                self.meow.play()
                time.delay(2000) # adds a delay before exiting the game
                self.end_game = True

    def render_you_win(self, surface, x, y, condition):
        if condition:

            # first displays pentagram for a short period of time, then the dead cat image and the message
            self.counter += 1
            self.counter_2 += 1
            if self.counter <= 10:
                self.background_song.stop()
                surface.blit(self.pentagram, (x, y))
            else:
                surface.blit(self.dead_cat, (x - 50, y - 150))
                surface.blit(self.messages[1], (x + 140, y + 350))

            if self.counter_2 > 12:
                self.lose_sound.play()
                time.delay(2000)
                self.end_game = True


