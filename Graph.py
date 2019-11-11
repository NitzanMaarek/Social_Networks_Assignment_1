import pandas as pd
import os
import Node

class Graph:

    def __init__(self):
        self.number_of_nodes = 0
        self.graph_dict = {}

    def load_graph(self, path):
        """
        Loads a graph from a text file to the memory.
        :param path: path of file.
        :return:
        """
        if path is None or not os.path.isfile(path):
            return 'Path not found.'
        df = pd.read_csv(path, header=None)
        for index, row in df.iterrows():
            source = row[0]
            dest = row[1]
            if source not in self.graph_dict.keys():
                self.graph_dict[source] = set()        #Initializing set
            self.graph_dict[source].add(dest)
        df = pd.read_csv(path)
        self.graph_dict = dict()


    def calculate_page_rank(self, beta=0.85, delta=0.001, max_iterations=20):
        self.reset_page_rank_values()
        iter_delta = 1
        for i in range(20) and iter_delta > delta: # TODO: Check this row
            iter_delta = self.page_rank_iteration(beta)

    def reset_page_rank_values(self):
        init_pr = 1 / self.number_of_nodes
        for node in self.graph_dict.items():
            node.set_page_rank(init_pr)

    def page_rank_iteration(self, beta=0.85):
        new_pr_values = dict()
        total_delta = 0
        for node in self.graph_dict.items():
            new_pr = 0
            for neighbor in node.neighbors:
                neighbor_node = self.graph_dict[neighbor]
                new_pr += neighbor_node.get_page_rank / neighbor_node.degree
            new_pr = new_pr * beta
            new_pr_values[node.name] = new_pr
            total_delta += abs(node.get_page_rank() - new_pr)

        for node in self.graph_dict.items():
            node.set_page_rank(new_pr_values[node.name])

        return total_delta

    def get_page_rank(self, node_name):
        return self.graph_dict[node_name].get_page_rank()

if __name__ == '__main__':
    graph = Graph()
    graph.load_graph(r'C:\Users\nitsa\Desktop\Wikipedia_votes.csv')