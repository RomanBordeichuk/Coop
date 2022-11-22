from .RoadInstance import Road
from .NodeInstance import Node
from .Algorithms import GraphAlgorithms
from .Consts import NameMapFile
import json


class Map:

    n_nodes: int
    n_roads: int
    n_cars: int
    nodes: list[Node] = []
    spawn_nodes: list[int] = []
    roads: list[Road] = []
    offset_x: float = 0.0
    offset_y: float = 0.0
    # distance_matrix = []

    @staticmethod
    def init(Ncars):
        Map.n_nodes = len(Map.nodes)
        Map.n_roads = len(Map.roads)
        Map.n_cars = Ncars
        #Map.distance_matrix = GraphAlgorithms.getMatrix(Map.nodes, Map.roads)