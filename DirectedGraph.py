from search import *
from hotelAndScenery import *
from anytime_algo import *
import random


class DirectedGraph(StateSpace):
    def __init__(self, action, gval, parent, node, start):
        StateSpace.__init__(self, action, gval, parent)
        self.action = action
        self.gval = gval
        self.parent = parent
        self.vertices = []
        self.edges = {}
        self.node = node
        self.start = start

    def successors(self):

        successors = []
        for node in self.vertices:
            if node != self.node:
                weight = dict_weight[(self.node, node)]
                state = DirectedGraph(self.action, self.gval + weight, self, node, self.start)
                vertices = self.vertices.copy()
                vertices.remove(self.node)
                state.create_vertices_list(vertices)
                state.create_edges_list(self.edges)
                if tsp_goal_state(state):
                    return_weight = dict_weight[(state.node, state.start)]
                    state = DirectedGraph(state.action, state.gval + return_weight, state.parent, state.node, state.start)
                    state.create_vertices_list(vertices)
                    state.create_edges_list(self.edges)
                successors.append(state)
        return successors

    def print_path(self):
        temp = self
        print("Total time spend on road is {} mins.".format(temp.gval))
        print("=======================================================")
        print(dict_name[temp.start], "to", dict_name[temp.node], "takes",
              dict_weight[(temp.node, temp.start)], "mins.")
        while temp:
            if temp.parent:
                print(dict_name[temp.node], "to", dict_name[temp.parent.node], "takes",
                      dict_weight[(temp.parent.node, temp.node)], "mins.")
            temp = temp.parent

    def hashable_state(self):
        return hash(self.node + str(len(self.vertices)))

    def create_vertices_list(self, vertices):
        self.vertices = vertices

    def create_edges_list(self, edges):
        self.edges = edges

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, node1, node2, weight):
        self.edges[(node1, node2)] = weight
        self.edges[(node2, node1)] = weight

    def get_vertices(self):
        return self.vertices

    def get_weight(self, edge):
        return self.edges[edge]

    def get_edges(self):
        return self.edges


def tsp_goal_state(state):
    return len(state.get_vertices()) == 1
