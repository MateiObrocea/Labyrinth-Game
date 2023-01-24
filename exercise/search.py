import bisect


class Search:
    """
    Class which computes the movement algorithm of the chaser
    When the path becomes short enough, the game is lost
    """

    def __init__(self, graph):
        self.graph = graph
        self.get_caught_condition = False # sets the condition for losing the game

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

        if len(visited) <= 1:
            self.get_caught_condition = True

        # self.highlight_path()

    def highlight_path(self):
        # Compute the path, back to front.
        current_node = self.graph.target.parent
        while current_node is not None and current_node != self.graph.start:
            current_node.set_color((248, 220, 50))
            current_node = current_node.parent

    def get_path(self):
        # Computes and returns the path
        current_node = self.graph.target.parent
        path = []
        while current_node is not None and current_node != self.graph.start:
            path.append(current_node.position)
            current_node = current_node.parent
        return path
