import random
import time
from datetime import datetime

import pygame.time

from exercise.maze import Maze
import bisect
import sys


class Search:

    def __init__(self, graph):
        self.graph = graph
    # def breadth_first_solution(self):
    #
    #     self.graph.reset_state()
    #
    #     queue = [self.graph.start]
    #     visited = []
    #
    #     while len(queue) > 0:
    #         current_node = queue.pop(0)
    #         if current_node != self.graph.target:
    #             if current_node not in visited:
    #                 visited.append(current_node)
    #                 neighbours = current_node.get_neighbours()
    #                 random.shuffle(neighbours)
    #                 for next_node in neighbours:
    #                     if next_node not in visited:
    #                         next_node.set_parent(current_node)
    #                         queue.append(next_node)
    #         else:
    #             break
    #     print("The number of visited nodes is: {}".format(len(visited)))
    #     self.highlight_path()
    #
    # def depth_first_solution(self):
    #
    #     self.graph.reset_state()
    #
    #     stack = [self.graph.start]
    #     visited = []
    #
    #     while len(stack) > 0:
    #         current_node = stack.pop()
    #         if current_node != self.graph.target:
    #             if current_node not in visited:
    #                 visited.append(current_node)
    #                 neighbours = current_node.get_neighbours()
    #                 # random.shuffle(neighbours)
    #                 for next_node in neighbours:
    #                     if next_node not in visited:
    #                         next_node.set_parent(current_node)
    #                         stack.append(next_node)
    #         else:
    #             break
    #     print("The number of visited nodes is: {}".format(len(visited)))
    #     self.highlight_path()
    #
    # # ADD YOU IMPLEMENTATIONS FOR GREEDY AND ASTAR HERE!
    # def greedy_search(self):
    #     self.graph.reset_state()
    #
    #     queue = [self.graph.start]
    #     visited = []
    #
    #     while len(queue) > 0:
    #         current_node = queue.pop(0)
    #         if current_node != self.graph.target:
    #             if current_node not in visited:
    #                 visited.append(current_node)
    #                 neighbours = current_node.get_neighbours()
    #                 for next_node in neighbours:
    #                     if next_node not in visited:
    #                         next_node.set_parent(current_node)
    #                         score = self.graph.target.manhattan_distance(next_node)
    #                         next_node.set_score(score)
    #                         bisect.insort_left(queue, next_node)
    #         else:
    #             break
    #     print("The number of visited nodes is: {}".format(len(visited)))
    #     self.highlight_path()

    def a_star_search(self):
        self.graph.reset_state()
        queue = [self.graph.start]
        visited = []
        self.highlight_path()
        while len(queue) > 0:
            current_node = queue.pop(0)
            if current_node != self.graph.target:
                if current_node not in visited:
                    visited.append(current_node)
                    neighbours = current_node.get_neighbours()
                    for next_node in neighbours:
                        if next_node not in visited:
                            gscore = self.graph.target.manhattan_distance(next_node)
                            fscore = current_node.get_distance() + 1
                            score = fscore + gscore
                            if next_node not in queue:
                                next_node.set_parent(current_node)
                                next_node.set_score(score)
                                bisect.insort_left(queue, next_node)
                            elif fscore < next_node.get_distance():
                                next_node.set_parent(current_node)
                                next_node.set_score(score)
                                queue.remove(next_node)
                                bisect.insort_left(queue, next_node)


            else:
                break
        # print("The number of visited nodes is: {}".format(len(visited)))
        self.highlight_path()
        # return self.get_path()

    def highlight_path(self):
        # Compute the path, back to front.
        current_node = self.graph.target.parent
        while current_node is not None and current_node != self.graph.start:
            current_node.set_color((248, 220, 50))
            # pygame.time.wait(10)
            current_node = current_node.parent

    def get_path(self):
        # Computes and returns the path
        current_node = self.graph.target.parent
        path = []
        while current_node is not None and current_node != self.graph.start:
            path.append(current_node.position)
            current_node = current_node.parent
        return path
