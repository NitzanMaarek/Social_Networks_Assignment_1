import pandas as pd
import os
from Node import Node
from heapq import heappop, heappush, heapreplace

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
                node = Node(source_node_name)
                # self.graph_dict[source] = set()        #Initializing set
                self.graph_dict[source_node_name] = node
            self.graph_dict[source_node_name].add_neighbor(dest_node_name)

            # We must add nodes which have only in edges because their might be dead ends in the graph
            if dest_node_name not in self.graph_dict.keys():
                node = Node(dest_node_name)
                self.graph_dict[dest_node_name] = node

            self.graph_dict[dest_node_name].degree += 1

        self.number_of_nodes = len(self.graph_dict.keys())
        print(self.graph_dict)

    def calculate_page_rank(self, beta=0.85, delta=0.001, max_iterations=20):
        self.reset_page_rank_values()
        iter_delta = 1
        for i in range(max_iterations):
            if iter_delta > delta:
                iter_delta = self.page_rank_iteration(beta)
                print('iter number ' + str(i) + ' done')
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
            if len(node.neighbors_set) > 0:
                added_pr_value = (float(node.page_rank) / float(len(node.neighbors_set))) * beta
                for neighbor in node.neighbors_set:
                    neighbor_node = self.graph_dict[neighbor]
                    if neighbor_node.name not in new_pr_values.keys():
                        new_pr_values[neighbor_node.name] = 0
                    new_pr_values[neighbor_node.name] += added_pr_value
                    total_pr += added_pr_value

        leak_value = float(1 - total_pr) / self.number_of_nodes

        for node_name, node in self.graph_dict.items():
            if node_name in new_pr_values.keys():
                new_pr_added_leak = new_pr_values[node.name] + leak_value
            else:
                new_pr_added_leak = leak_value
            total_delta += abs(new_pr_added_leak - node.page_rank)
            node.set_page_rank(new_pr_added_leak)



        return total_delta

    def get_page_rank(self, node_name):
        return self.graph_dict[node_name].get_page_rank()

    def get_top_nodes(self, n):
        nodes_n_heap = [] #heap
        top_n_nodes = []
        max_page_rank = 0
        for key in self.graph_dict:
            value = self.graph_dict[key]
            if value.get_page_rank() > max_page_rank:
                max_page_rank = value.get_page_rank()
            page_rank_node_name_tuple = (value.get_page_rank(), key)
            if n >= 0:   # set heap size to n
                heappush(nodes_n_heap, page_rank_node_name_tuple)
                n -= 1
            else:       # keep heap size to n
                heapreplace(nodes_n_heap, page_rank_node_name_tuple)
        heappop(nodes_n_heap)   # Make sure we have top n nodes, so we had n+1 in heap so we wont pop the last node.
        self.switch_tuple_items(nodes_n_heap, top_n_nodes)
        print("Max page rank for confirmation is: " + str(max_page_rank))
        return list(reversed(top_n_nodes))

    def switch_tuple_items(self, nodes_heap, top_n_nodes):
        while nodes_heap:
            page_rank_node_name_tuple = heappop(nodes_heap)
            node_name_to_page_rank = (page_rank_node_name_tuple[1], page_rank_node_name_tuple[0])
            top_n_nodes.append(node_name_to_page_rank)

    def get_all_page_rank(self):
        ### NEED TO TEST THIS METHOD ###
        page_rank_to_node_name_heap = []
        node_name_to_page_rank = []
        for key in self.graph_dict:
            page_rank = self.graph_dict[key].get_page_rank()
            page_rank_node_name = (page_rank, key)
            heappush(page_rank_to_node_name_heap, page_rank_node_name)
        self.switch_tuple_items(page_rank_to_node_name_heap, node_name_to_page_rank)
        return list(reversed(node_name_to_page_rank))

if __name__ == '__main__':
    graph = Graph()
    graph.load_graph(r'C:\Chen\BGU\2020\2020 - A\Social Networks Analysis\Assignments\Social_Networks_Assignment_1\Wikipedia_votes.csv')
    # graph.load_graph(r"C:\Users\nitsa\Desktop\Wikipedia_votes.csv")
    graph.calculate_page_rank()
    # print(graph.get_page_rank(271))
    print(graph.get_top_nodes(20))
    # print(graph.get_all_page_rank())
    s = 0
    for node_name, node in graph.graph_dict.items():
        s += node.get_page_rank()
    print s
