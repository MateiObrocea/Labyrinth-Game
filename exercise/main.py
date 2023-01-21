import pygame
import sys
from exercise.helpers.keyboard_handler import KeyboardHandler
from exercise.maze import Maze
from exercise.helpers.constants import Constants
from exercise.search import Search
from CameraDetection import CameraDetection



class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """
    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.keyboard_handler = KeyboardHandler()
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)
        self.time = pygame.time.get_ticks()
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_maze()
        self.search = Search(self.maze)
        self.player_x = 0
        self.player_y = 0
        self.target_x = 12
        self.target_y = 12
        self.last_move_time = pygame.time.get_ticks()
        self.camera = CameraDetection()

    """
    Method 'game_loop' will be executed every frame to drive
    the display and handling of events in the background. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.handle_events()
        self.update_game()
        self.draw_components()
        self.maze.set_target(self.maze.grid[self.target_x][self.target_y])
        self.maze.set_source(self.maze.grid[self.player_x][self.player_y])
        self.search.a_star_search()
        # print(self.last_move_time)
        self.camera.perform()



        # for neighbor in self.maze.grid.neighbours:
        #     if self.maze.direction(neighbor) == (0, -1):  # North
        #         self.player_y = self.player_y - 1
        #     elif self.maze.grid.direction(neighbor) == (1, 0):  # East
        #         self.player_x = self.player_x + 1
        #     elif self.maze.grid.direction(neighbor) == (0, 1):  # South
        #         self.player_y = self.player_y + 1
        #     elif self.maze.grid.direction(neighbor) == (-1, 0):  # West
        #         self.player_x = self.player_x - 1

    """
    Method 'update_game' is there to update the state of variables 
    and objects from frame to frame.
    """
    def update_game(self):
        # triggers the movement of the target at a certain speed
        current_time = pygame.time.get_ticks()

        if current_time - self.last_move_time > 100:
            self.move_target()
            self.move_player()
            self.last_move_time = current_time

    def move_player(self):
        if self.camera.direction == 2 and self.target_y > 0:
            self.target_y = self.target_y - 1
        if self.camera.direction == 0 and self.target_x < Constants.GRID_COLS - 1:
            self.target_x = self.target_x + 1
        if self.camera.direction == 3 and self.target_y < Constants.GRID_ROWS - 1:
            self.target_y = self.target_y + 1
        if self.camera.direction == 1 and self.target_x > 0:
            self.target_x = self.target_x - 1



    """
    Method 'draw_components' is similar is meant to contain 
    everything that draws one frame. It is similar to method
    void draw() in Processing. Put all draw calls here. Leave all
    updates in method 'update'
    """
    def move_target(self):
        # moves the target towards the player
        path = self.search.get_path()
        if path:
            for node in path:
                self.player_x = node[0]
                self.player_y = node[1]

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)
        pygame.display.flip()

    def draw_score(self):
        text = self.font.render(str(self.maze.target.distance), True, (0,0,0))
        self.screen.blit(text, (self.size[0]/2-64, 20))

    def reset(self):
        pass

    """
    Method 'handle_event' loop over all the event types and 
    handles them accordingly. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """
    def handle_key_down(self, event):


        self.keyboard_handler.key_pressed(event.key)
        if event.key == pygame.K_m:
            print("Generating Maze")
            self.maze.generate_maze()
        if event.key == pygame.K_o:
            print("Generating Obstacle")
            self.maze.generate_obstacles()
        if event.key == pygame.K_r:
            print("Generating Rooms")
            self.maze.generate_room()
        if event.key == pygame.K_b:
            print("BFS")
            self.search.breadth_first_solution()
        if event.key == pygame.K_d:
            print("DFS")
            self.search.depth_first_solution()
        if event.key == pygame.K_g:
            print("Greedy")
            self.search.greedy_search()

        # player control
        if event.key == pygame.K_UP and self.target_y > 0:
            self.target_y = self.target_y - 1
        if event.key == pygame.K_RIGHT and self.target_x < Constants.GRID_COLS - 1:
            self.target_x = self.target_x + 1
        if event.key == pygame.K_DOWN and self.target_y < Constants.GRID_ROWS - 1:
            self.target_y = self.target_y + 1
        if event.key == pygame.K_LEFT and self.target_x > 0:
            self.target_x = self.target_x - 1

    """
    This method will remove a released button 
    from list 'keyboard_handler.pressed'.
    """

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)



    """
    Similar to void mouseMoved() in Processing
    """
    def handle_mouse_motion(self, event):
        pass

    """
    Similar to void mousePressed() in Processing
    """
    # def handle_mouse_pressed(self, event):
    #     x = int(event.pos[0] / self.maze.cell_width)
    #     y = int(event.pos[1] / self.maze.cell_height)
    #     if event.button == 1:
    #         self.maze.set_source(self.maze.grid[x][y])
    #     if event.button == 3:
    #         self.maze.set_target(self.maze.grid[x][y])

    """
    Similar to void mouseReleased() in Processing
    """
    def handle_mouse_released(self, event):
        pass


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
