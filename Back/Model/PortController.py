from typing import Counter
from .Util.MapController import Map
from .CarController import CarDriver
from .LightsController import LightsController
from .Util.NodeInstance import Node
from .Util.RoadInstance import Road
from .Util.Consts import *
from .Util.Algorithms import excludeOSMGraph
from .config import *
import time

import json
import osmnx

count = 1

class PortDriver:

    @staticmethod
    def getCarsIntoFile(): # cars into file.json for simulation
        row = []

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x != -1:
                row.append({ car_index : [car.getCoordinates(), [car.getRoad().start_node, car.getRoad().end_node], car.color]} )

        data = json.dumps({"cars": row})
        
        return data
        #print(data)
        # ServerRabbit.sendData(data, 'cars')

    @staticmethod
    def getCarsIntoFile3D(): # cars into file.json for simulation 3d
        row = []

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x != -1:
                row.append({ car_index : [car.getCoordinatesReal(), [car.getRoad().start_node, car.getRoad().end_node], car.color]} )

        data = json.dumps({"cars": row})
        
        return data

    def getLightsIntoFile():

        return LightsController.getLigths()

    @staticmethod
    def getMapIntoFile():  # all graph into file.json for simulation
        row_nodes = []
        row_roads = {}

        for node in Map.nodes:
            row_nodes.append([node.apos, node.type])
            temp = {}
            for road in node.start_roads:
                temp[road.end_node] = [road.n_lines, road.angle, road.index, road.is_open]

            row_roads[node.index] = temp

        # data = json.dumps({"nodes": row_nodes, "roads": row_roads})

        return {"nodes": row_nodes, "roads": row_roads}
        # ServerRabbit.sendData(data, 'cars') 


    @staticmethod
    def setMapByName(Name):
        graph = osmnx.graph_from_place(Name, simplify=True, network_type='drive')

        Map.nodes, Map.spawn_nodes, Map.roads, Map.offset_x, Map.offset_y = excludeOSMGraph(graph)

    @staticmethod
    def setMapFromFile(fileName):
        
        start = time.time()

        if '.json' in fileName:
            import_file = open(fileName, 'r')

            data = json.load(import_file)

            row_nodes = data['nodes']
            row_roads = data['roads']

            Map.nodes = []
            Map.roads = []
            Map.spawn_nodes = []

            for node_index, node in enumerate(row_nodes):
                Map.nodes.append(Node(node[1], node[0], node_index))
                if Map.nodes[-1].type == 0:
                    Map.spawn_nodes.append(Map.nodes[-1].index)


            for road in row_roads:
                s_n = road[0][0]
                e_n = road[0][1]
                Map.roads.append(Road(Map.nodes, s_n, e_n, road[1]))
                Map.nodes[s_n].addRoad(Map.roads[-1])
                Map.nodes[e_n].addRoad(Map.roads[-1], 'end')

            #Map.init(nodes, spawn_nodes, roads)
            import_file.close()
            return [Map.nodes, Map.spawn_nodes, Map.roads]


        elif '.osm' in fileName: # from .osm
            graph = osmnx.graph_from_xml(fileName, simplify=True)

            Map.nodes, Map.spawn_nodes, Map.roads, Map.offset_x, Map.offset_y  = excludeOSMGraph(graph, use_custom_algorithm=True)

        else: # from .txt
            graph = open(fileName, 'r')

            n_nodes, n_roads, n_cars = list(map(int, graph.readline().split()))

            Map.nodes = [None] * n_nodes
            Map.spawn_nodes = []
            Map.roads = [None] * n_roads

            for i in range(n_nodes):
                type_name, x, y = list(map(int, graph.readline().split()))  # types: 0 - spawn, 1 - intersect
                node = Node(type_name, (x, y), i)
                Map.nodes[i] = node

                if type_name == 0:
                    Map.spawn_nodes.append(i)

            for i in range(n_roads):
                s_n, e_n, n_lines = list(
                    map(int,
                        graph.readline().split()))  # start node, end node, length, number of lines, absolute position
                road = Road(Map.nodes, s_n, e_n, n_lines // 2 if n_lines > 1 else n_lines)
                Map.roads[i] = road

                Map.nodes[s_n].addRoad(road)
                Map.nodes[e_n].addRoad(road, 'end')

                if n_lines > 1:
                    reverse_road = Road(Map.nodes, e_n, s_n, n_lines // 2)
                    Map.roads.append(reverse_road)
                    Map.nodes[e_n].addRoad(reverse_road)
                    Map.nodes[s_n].addRoad(reverse_road, 'end')

            graph = None
            #Map.init(nodes, spawn_nodes, roads)
            return [Map.nodes, Map.spawn_nodes, Map.roads]

        print("The time for graph creating: ", abs(time.time() - start))

    @staticmethod
    def parse_cars(cars):
        # input {"cars" {{car_id : [[[ax, ay], angle, speed], [start_node, end_node]]}}
        # output {"car_id" : "x" : ax, "y" : ay, "angle" : angle, "speed" : speed, "start node" : s_node, "end node" : e_node}
        parsed_cars = dict()
        for car in cars["cars"]:
            car_index = list(car.keys())[0]
            car_instance = car[car_index]

            parsed_cars[car_index] = {
                "x" : car_instance[0][0][0],
                "y" : car_instance[0][0][1],
                "angle": car_instance[0][1],
                "speed" : car_instance[0][2],
                "start node" : car_instance[1][0],
                "end node" : car_instance[1][1] 
            }
        return parsed_cars
        
    @staticmethod
    def parse_lights(lights):
        #This is parsing data for making a table out of it so I don't care about sublights and roads? Idk, anyway this can be easily changed to get it too
        # input -> [[id, sublights, periods, is_first_open, counter]]
        # output -> {id : {"periods": periods, "state" : is_first_open, "counter" : counter}
        
        parsed_lights = dict()
        for light in lights:
            light_id = light[0]
            parsed_lights[light_id] = {
                "periods" : light[3],
                "state" : light[4], 
                "counter" : light[5]
            }


        return parsed_lights
        
        
        
        # sublight -> list[[x, y], angle, color]
        return [self.id, sublights, self.array_roads, self.periods, self._is_first_open, self.counter]

    
    @staticmethod
    def price_counter():
        global count
        string = f'Traffic lights - {count * 2}$; Adjuster - {count * 1.25}$'

        count += 1
        return string