import pandas as pd
import os
from Node import Node

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
            source_node_name = row[0]
            dest_node_name = row[1]
            if source_node_name not in self.graph_dict.keys():
                node = Node(set(), source_node_name)
                # self.graph_dict[source] = set()        #Initializing set
                self.graph_dict[source_node_name] = node
            self.graph_dict[source_node_name].add_neighbor(dest_node_name)

            # We must add nodes which have only in edges because their might be dead ends in the graph
            if dest_node_name not in self.graph_dict.keys():
                node = Node(set(), dest_node_name)
                self.graph_dict[dest_node_name] = node

        self.number_of_nodes = len(self.graph_dict.keys())
        print(self.graph_dict)



    def calculate_page_rank(self, beta=0.85, delta=0.001, max_iterations=20):
        self.reset_page_rank_values()
        iter_delta = 1
        for i in range(20): # TODO: Check this row
            if iter_delta > delta:
                iter_delta = self.page_rank_iteration(beta)
                print 'iter number ' + str(i) + ' done'
            else:
                break

    def reset_page_rank_values(self):
        init_pr = float(1) / float(self.number_of_nodes)
        for node_name, node in self.graph_dict.items():
            node.set_page_rank(init_pr)

    def page_rank_iteration(self, beta=0.85):
        new_pr_values = dict()
        total_delta = 0
        total_pr = 0
        for node_name, node in self.graph_dict.items():
            new_pr = 0
            for neighbor in node.neighbors_set:
                neighbor_node = self.graph_dict[neighbor]
                if neighbor_node.degree != 0:
                    new_pr += float(neighbor_node.get_page_rank) / float(neighbor_node.degree)
            new_pr = new_pr * beta
            new_pr_values[node.name] = new_pr
            total_pr += new_pr
            total_delta += abs(node.get_page_rank() - new_pr)

        leak_value = float(1 - total_pr) / self.number_of_nodes

        for node_name, node in self.graph_dict.items():
            new_pr_no_leak = new_pr_values[node.name] + leak_value
            node.set_page_rank(new_pr_no_leak)

        return total_delta

    def get_page_rank(self, node_name):
        return self.graph_dict[node_name].get_page_rank()

if __name__ == '__main__':
    graph = Graph()
    graph.load_graph(r'C:\Chen\BGU\2020\2020 - A\Social Networks Analysis\Assignments\Social_Networks_Assignment_1\Wikipedia_votes.csv')
    graph.calculate_page_rank()
    print graph.get_page_rank(271)