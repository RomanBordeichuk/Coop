from typing import Tuple
from .NodeInstance import Node
from .MapController import Map
from.LineInstance import Line
from .RoadInstance import Road
from .Consts import PeriodStopFlow, IngnoringSupreme
from math import pi, cos, sin

class TrafficLight:
    # Lines, which connected to node, separated into two arrays:
    array_roads : list[list[Road], list[Road]] = [[], []]

    # Those arrays represent the separation for traffic light
    # We declare that traffic light has two periods
    periods : list[int, int]
    _is_first_open : bool = True
    counter : int = 0

    # When period one changes : traffic light 1 and 3 (2 and 4) change the colours to green (red)
    #                           traffic light 2 and 4 (1 and 3) change the colours to red (green)
    # For the another period : just vice versa
    #
    #           |   |
    #           |   |
    #           |(2)|
    # ======(3)=     =(1)=====
    #           |(4)|
    #           |   |
    #           |   |
    # /X-intersection by invalid art creator/
    #
    # For lines stopping implementation we will just change the last cell in lines
    # (for instance, line = [0, 0, 0, 1, 0, 0] -> [0, 0, 0, 1, 0, 1])


    # class Controller which created for regulation of traffic flow
    # The main idea of this: We have open group of roads
    # Stop flow in first road for const time, after that
    # vice versa for another road
    # But the cycle might change because of condition (if here's one road, if one road has density == 0)

    # Simple enough, if I work out something more reasonable for our purposes, I'll write it down
    class Controller:
        def __init__(self, group_roads: list[list[Road]]) -> None:
            self._period_stopping = PeriodStopFlow
            self._ignoring_sup = IngnoringSupreme
            self._group_roads = group_roads
            self._first_road_stopped = False
            self._timer = 0

        def changeLine(self):
            self._first_road_stopped = False
            self._timer = 0

        def change(self, is_first_open):
            # firstly, change timers
            group_bools1 = [False] * len(self._group_roads[0])
            group_bools2 = [False] * len(self._group_roads[1])
            
            for road in self._group_roads[int(not is_first_open)]:
                road.Flow()

            if is_first_open:
                if len(group_bools1) >= 2:
                    if self._first_road_stopped:
                        if self._group_roads[0][0].K < self._ignoring_sup: # We need to add "seeing" if line's end is busy
                            group_bools1[0] = True
                        group_bools1[1] = True
                    else:
                        if self._group_roads[0][1].K < self._ignoring_sup:
                            group_bools1[1] = True
                        group_bools1[0] = True
                else:
                    group_bools1 = [True]

            else:
                if len(group_bools2) >= 2:
                    if self._first_road_stopped:
                        if self._group_roads[1][0].K < self._ignoring_sup: # We need to add "seeing" if line's end is busy
                            group_bools2[0] = True
                        group_bools2[1] = True
                    else:
                        if self._group_roads[1][1].K < self._ignoring_sup:
                            group_bools2[1] = True
                        group_bools2[0] = True
                else:
                    group_bools2 = [True]

            self._timer += 1
            if self._timer > self._period_stopping:
                self._first_road_stopped = not self._first_road_stopped
                self._timer = 0

            # and then change roads' stop signals 
            for index, flag in enumerate(group_bools1):
                if not flag:
                    road = self._group_roads[0][index]
                    for line in road.lines[road.start_node]:
                        line.cells[-1] = 1
                else:
                    road = self._group_roads[0][index]
                    for line in road.lines[road.start_node]:
                        line.cells[-1] = 0
            
            for index, flag in enumerate(group_bools2):
                try:
                    if not flag:
                        road = self._group_roads[1][index]
                        for line in road.lines[road.start_node]:
                            line.cells[-1] = 1
                    else:
                        road = self._group_roads[1][index]
                        for line in road.lines[road.start_node]:
                            line.cells[-1] = 0
                
                except:
                    pass


    def __init__(self, light_id, array_of_roads,  init_periods, node_id):
        # In the beginning, we used random function for distribution of lines

        # sample_roads1 = sample(array_of_roads, len(array_of_roads) // 2)
        # sample_roads2 = [array_of_roads[i] for i, road in enumerate(array_of_roads) if not (road in sample_roads1)]
        #
        # self.array_roads = [sample_roads1, sample_roads2]

        # Another application of setting the roads into types
        # We implemented the algorithm that used finding delta angles of roads
        # That means if delta angle of two roads is more than 3*pi/4 and less than 5*pi/4,
        # we will insert those roads into the first group
        # (for example, the first road has angle equals 1 radian and the second road has angle 4 radians,
        # their delta angle equals 3 radians which satisfied our condition)


        self.id = light_id

        group1 = []
        group2 = []

        group1.append(array_of_roads[0])
        for road in array_of_roads[1:]:
            delta_angle = 4 * abs(road.angle - group1[0].angle)
            if delta_angle <= 5*pi and delta_angle >= 3*pi:
                group1.append(road)
            else:
                group2.append(road)

        self.array_roads = [group1, group2]


        # initializing the periods

        self.periods = init_periods
        self.node : Node = Map.nodes[node_id]
        self.center : int = Map.nodes[node_id].apos

        self.controller = self.Controller(self.array_roads)

    def ChangeLine(self):
        
        try:
            # if self._is_first_open:
            #     for road in self.array_roads[0]:
            #         for line in road.lines[road.start_node]:
            #             line.cells[-1] = 0
            #     for road in self.array_roads[1]:
            #         for line in road.lines[road.start_node]:
            #             line.cells[-1] = 1
            # else:
            #     for road in self.array_roads[1]:
            #         for line in road.lines[road.start_node]:
            #             line.cells[-1] = 0
            #     for road in self.array_roads[0]:
            #         for line in road.lines[road.start_node]:
            #             line.cells[-1] = 1

            self.controller.changeLine()
        except:
            print("Captured some inadequate problems with traffic lights")

        self._is_first_open = not self._is_first_open

    def Change(self):
        self.counter += 1
        flag = int(self._is_first_open)
        if self.counter >= self.periods[flag]:
            self.counter = 0
            self.ChangeLine()
            
        self.controller.change(self._is_first_open)


    def getAttributes(self):
        
        sublights = []

        for index, array_road in enumerate(self.array_roads):
            for road in array_road:
                sublight = []
                colorset = ['green', 'yellow', 'red']
                color = None

                R = 15
                offset = 7
                x = self.center[0] - R*cos(road.angle + pi) + offset * sin(road.angle)
                y = self.center[1] - R*sin(road.angle + pi) - offset * cos(road.angle)
                angle = road.angle - pi / 2
                sublight.append([x, y])
                sublight.append(angle)

                if index == 0:
                    if self._is_first_open:
                        color = colorset[0]
                    else:
                        color = colorset[1] if self.counter >= self.periods[index] - 1 else colorset[2]
                else:
                    if not self._is_first_open:
                        color = colorset[0]
                    else:
                        color = colorset[1] if self.counter >= self.periods[index] - 1 else colorset[2]

                sublight.append(color)

                sublights.append(sublight)

        # sublight -> list[list[x, y], angle, color]
        return [self.id, sublights, self.array_roads, self.periods, self._is_first_open, self.counter, self.node]

