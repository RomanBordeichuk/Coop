from start import info
from .Consts import *
from .NodeInstance import Node
from .RoadInstance import Road
from .TrafficLightInstance import TrafficLight
import math

# The main module for advanced algorithms which created for solving the 6th task.
# It includes DFSRoads for optimizing (vertexes and edges compressing) a traffic system
# Of course, It includes GA algorithm 

class AdvancedGraphAlgorithms:

    @staticmethod
    def DFSRoads(roads, start_node, roads_colored):
        path = []
        lenght = 0
        max_velocity = MaxVelocity
        n_lines = math.inf

        
class OptimizedNode:
    def __init__(self, node: Node, traffic_light: TrafficLight = None):
        self.index = node.index
        self.adj_roads = node.adj_nodes
        self._traffic_light = traffic_light


class OptimizedRoad:
    def __init__(self, length: int, max_velocity: int, n_lines: int, start_node: int, end_node: int):
        self.length = length
        self.max_velocity = max_velocity
        self.n_lines = n_lines
        self.start_node = start_node
        self.end_node = end_node

    def getFlow(self):
        pass

    def getDensity(self):
        pass


class OptimizedGraph:

    def InitGraph(nodes: list[Node], roads: list[Road]):
        pass