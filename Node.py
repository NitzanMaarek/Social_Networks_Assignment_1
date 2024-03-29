"""
Node class that represents a single Node in the graph.
Each Node has it's current page rank from the last page rank calculation and a list of its neighbors.
"""

class Node:

    def __init__(self, name):
        self.neighbors_set = set()
        self.page_rank = -1
        self.name = name
        # self.degree = len(neighbors)
        self.degree = 0

    def set_page_rank(self, page_rank):
        self.page_rank = page_rank

    def get_page_rank(self):
        return self.page_rank

    def add_neighbor(self, neighbor):
        self.neighbors_set.add(neighbor)
