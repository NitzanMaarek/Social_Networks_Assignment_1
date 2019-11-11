import pandas as pd
import os

class Graph:

    def __init__(self):
        self.number_of_nodes = 0

    def load_graph(self, path):
        """
        Loads a graph from a text file to the memory.
        :param path: path of file.
        :return:
        """
        if path is None or not os.path.isfile(path):
            return 'Path not found.'
        df = pd.read_csv(path)



if __name__ == '__main__':
