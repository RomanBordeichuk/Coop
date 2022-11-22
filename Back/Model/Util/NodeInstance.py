from .CarInstance import Car
from .RoadInstance import Road
from .LineInstance import Line
from random import sample


types = ["spawn", "intersect"]


class Node:

    def __init__(self, type, apos, index):
        self.type = types[type]  # 'spawn', 'intersect'
        self.apos = list(map(int, apos))  # absolute position (x, y)
        self.start_roads: list[Road] = [] # connected from: ->
        self.end_roads: list[Road] = [] # connected to: <-

        self.adj_nodes: list[list[int, Road]] = []
        self.queue: list[Car] = []
        self.n_parking_places = 1
        self.attributes = []
        self.index: int = index
        # self.traffic_light = TrafficLight() if self.type == 'spawn' else self.traffic_light = None

    def addRoad(self, road: Road, type='start'):
        if type == 'start':
            self.start_roads.append(road)
        else:
            self.end_roads.append(road)

    def addRoadAdj(self, end_node, road):
        self.adj_nodes.append([end_node, road])