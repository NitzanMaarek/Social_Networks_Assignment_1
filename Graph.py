import pandas as pd
import os

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

if __name__ == '__main__':
    graph = Graph()
    graph.load_graph(r'C:\Users\nitsa\Desktop\Wikipedia_votes.csv')