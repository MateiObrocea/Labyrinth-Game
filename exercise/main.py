"""
    Artificial Intelligence & Programming final project
    Represents a chasing game on a grid-like map, where a cat tries to catch a bird
    The player controls the bird with an arrow via the OpenCv library, such that the bird moves in the arrow direction
    The cat chases the bird
    Built upon the backbone of week 6 search assignment
    Authors: M.Obrocea and D.Yokubova
    24 - 01 - 2023

"""

import pygame
import sys
from exercise.helpers.keyboard_handler import KeyboardHandler
from exercise.maze import Maze
from exercise.helpers.constants import Constants
from CameraDetection import CameraDetection
from player import Player
from enemy import Enemy
from star import Star
from ui import UI


class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """

    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        """
        Loads all the components
        """
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.player = Player(12, 12, (Constants.CELL_SIZE, Constants.CELL_SIZE))
        self.chaser = Enemy(0, 0, (Constants.CELL_SIZE, Constants.CELL_SIZE), self.maze)

        self.star_list = []
        self.star_list.append(Star(Constants.GRID_COLS // 2, 12, (Constants.CELL_SIZE, Constants.CELL_SIZE)))
        self.star_list.append(Star(3, 9, (Constants.CELL_SIZE, Constants.CELL_SIZE)))
        self.star_list.append(Star(13, 9, (Constants.CELL_SIZE, Constants.CELL_SIZE)))
        self.star_list.append(Star(5, 3, (Constants.CELL_SIZE, Constants.CELL_SIZE)))
        self.star_list.append(Star(11, 3, (Constants.CELL_SIZE, Constants.CELL_SIZE)))

        self.keyboard_handler = KeyboardHandler()
        self.time = pygame.time.get_ticks()
        self.time_player = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()

        self.maze.generate_obstacles()

        self.user_interface = UI()
        self.camera = CameraDetection()


    """
    Generates the condition which stops the while loop
    """
    def game_exit(self):
        if self.user_interface.end_game:
            return True

    """
    Generates the condition for winning the game
    """
    def stars_collected(self):
        for i in range(5):
            if not self.star_list[i].is_collected:
                return False
        return True

    """
       Method 'game_loop' will be executed every frame to drive
       the display and handling of events in the background. 
       """

    def game_loop(self):
        self.handle_events()
        self.draw_components()
        self.update_game(Constants.PLAYER_SPEED, Constants.ENEMY_SPEED)
        self.camera.perform()

    """
    Method 'update_game' is there to update the state of variables 
    and objects from frame to frame.
    """

    def update_game(self, player_speed, enemy_speed):

        for star in self.star_list:
            star.get_collected(self.player.position_x, self.player.position_y)
        self.maze.set_target(self.maze.grid[self.player.position_x][self.player.position_y])
        self.maze.set_source(self.maze.grid[self.chaser.position_x][self.chaser.position_y])
        current_time = pygame.time.get_ticks()
        self.chaser.seek_player()

        """
        updates the state of the agents at a certain rate
        Similar to millis() manipulation in Arduino
        """
        if current_time - self.time > enemy_speed:
            self.chaser.move(self.camera.direction)
            self.time = current_time

        if current_time - self.time_player > player_speed:
            self.move_player()
            self.time_player = current_time

    def move_player(self):
        if self.camera.direction == 0 and self.player.position_y > 0:
            self.player.move(0)
        if self.camera.direction == 1 and self.player.position_x < Constants.GRID_COLS - 1:
            self.player.move(1)
        if self.camera.direction == 2 and self.player.position_y < Constants.GRID_ROWS - 1:
            self.player.move(2)
        if self.camera.direction == 3 and self.player.position_x > 0:
            self.player.move(3)

    """
    Method 'draw_components' is meant to contain 
    everything that draws one frame.
    """

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)

        for star in self.star_list:
            star.render(self.screen)

        self.player.draw_sprite(self.screen)
        self.chaser.draw_sprite(self.screen)

        self.user_interface.render_you_win(self.screen, 150, 170, self.stars_collected())
        self.user_interface.render_game_over(self.screen, 150, 50, self.chaser.search.get_caught_condition)
        pygame.display.flip()


    """
    The handle events are still here for demonstration purposes
    """

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """

    def handle_key_down(self, event):

        self.keyboard_handler.key_pressed(event.key)

        # player control - demo purposes
        if event.key == pygame.K_UP and self.player.position_y > 0:
            self.player.move(0)
        if event.key == pygame.K_RIGHT and self.player.position_x < Constants.GRID_COLS - 1:
            self.player.move(1)
        if event.key == pygame.K_DOWN and self.player.position_y < Constants.GRID_ROWS - 1:
            self.player.move(2)
        if event.key == pygame.K_LEFT and self.player.position_x > 0:
            self.player.move(3)


gameExit = False

if __name__ == "__main__":
    game = Game()
    while not gameExit:
        game.game_loop()
        if game.game_exit():
            # pygame.time.delay(1000)
            gameExit = True



