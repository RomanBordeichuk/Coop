from .RoadInstance import Road
from .LineInstance import Line
from .Consts import *
import random
from math import atan, pi, copysign



class Car:
    class WayNode:
        def __init__(self, road_piece: Road, start_node: int, end_node: int):
            self.road = road_piece
            self.start_node = start_node
            self.end_node = end_node

        def __str__(self):
            return str(self.start_node) + " " + str(self.end_node)

    def __init__(self, x, ax=None, ay=None):
        self._v = StartVelocity
        self._a = Acceleration
        self.pause = 0
        self.x = x
        self.apos = [ax, ay]
        self.way = []
        self.wayProgress = -1
        self.currentLine = -1
        self.next_x = -1
        self.home_node = None
        self.work_node = None
        self.delay = 0
        self.color = random.choice(["red", "green", "magenta", "blue"])

    def CompV(self, gap) -> int:
        max_velocity = min(MaxVelocity, self.getRoad().max_velocity)
        self._v = min(self._v + self._a, max_velocity)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= Probability * 10:
            self._v = max(self._v - 1, 0)

        return self._v + self.x

    def addWayNode(self, road_piece: Road, start_node: int, end_node: int):
        self.way.append(self.WayNode(road_piece, start_node, end_node))

    def __getNode(self) -> WayNode:
        if 0 <= self.wayProgress < len(self.way):
            return self.way[self.wayProgress]
        else:
            pass

    def getRoad(self) -> Road:
        if 0 <= self.wayProgress < len(self.way):
            return self.__getNode().road
        else:
            pass

    def getLines(self) -> list[Line]:
        if 0 <= self.wayProgress < len(self.way):
            return self.getRoad().lines[self.__getNode().start_node]
        else:
            return []

    def getCoordinates(self) -> list[list[int], int]: # apos, angle

        from .MapController import Map

        def shrink(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        current_node = self.__getNode()
        start_node = Map.nodes[current_node.start_node]
        end_node = Map.nodes[current_node.end_node]

        x = end_node.apos[0] - start_node.apos[0]
        y = end_node.apos[1] - start_node.apos[1]
        length = len(self.getLines()[0].cells)

        self.apos[0] = shrink(self.x / length, 0, 1, 1 / length, 1) * (x) + start_node.apos[0]
        self.apos[1] = shrink(self.x / length, 0, 1, 1 / length, 1) * (y) + start_node.apos[1]


        return [self.apos, (atan(y / x) + pi * (x < 0)) if x != 0.00 else copysign(pi / 2, y), self._v * Separation / Scale * 111] # 111 km per angle 

    
    def getCoordinatesReal(self) -> list[list[int], int]: # apos, angle
        from .MapController import Map

        def shrink(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
        def convertIntoReal(value, mode=0): # mode: 0 - x, 1 - y
            if mode == 0:
                return value / Scale + Map.offset_x
            else:
                return value / Scale + Map.offset_y

        current_node = self.__getNode()
        start_node = Map.nodes[current_node.start_node]
        end_node = Map.nodes[current_node.end_node]

        x = end_node.apos[0] - start_node.apos[0]
        y = end_node.apos[1] - start_node.apos[1]
        length = len(self.getLines()[0].cells)

        self.apos[0] = convertIntoReal(shrink(self.x / length, 0, 1, 1 / length, 1) * (x) + start_node.apos[0])
        self.apos[1] = convertIntoReal(shrink(self.x / length, 0, 1, 1 / length, 1) * (y) + start_node.apos[1], 1)


        return [self.apos, (atan(y / x) + pi * (x < 0)) if x != 0.00 else copysign(pi / 2, y), self._v * Separation / Scale * 111]