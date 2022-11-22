from .Util.Algorithms import GraphAlgorithms
from .Util.CarInstance import Car
from .Util.MapController import Map
from .Util.RoadInstance import Road
from .Util.LineInstance import Line
from .Util.Consts import *
from numba import jit, cuda
import os
import random
import json
from math import inf
import time

class CarDriver:
    cars_array: list[Car] = []

    @staticmethod
    def init():
        CarDriver.cars_array = []
        print(Map.n_cars, "cars in that simulation")
        start = time.perf_counter()
        way_counter = 0

        for i in range(Map.n_cars):
            home_node = random.choice(Map.spawn_nodes)
            work_node = random.choice([i for i in Map.spawn_nodes if i != home_node])
            start_counter = time.perf_counter()
            way = GraphAlgorithms.A_Star(Map.nodes, home_node, work_node)
            way_counter += time.perf_counter() - start_counter
            #print(way, "way")

            car = Car(-1)

            for x in way:
                car.addWayNode(x[0], x[1], x[2])

            car.pos = (0, None)
            car.home_node = home_node
            car.work_node = work_node

            Map.nodes[home_node].queue.append(car)
            Map.nodes[home_node].n_parking_places += 1
            CarDriver.cars_array.append(car)

            #CarDriver.assignCars()

        print(time.perf_counter() - start, "seconds for creating cars")
        print(way_counter, "seconds for creating ways for cars")

    @staticmethod
    def assignCars(): # assign cars from queue in spawn_nodes, which are home's, work's, and entertainment's park places

        for spawn_node in Map.spawn_nodes:
            queue_del = []
            for car in Map.nodes[spawn_node].queue:
                if car.delay > 0: # if car is not going anyway
                    car.delay -= 1
                    continue

                car.wayProgress = 0
                for line in car.getLines():
                    try:
                        if line.cells[0] == 0:
                            car.x = 0
                            line.cells[0] = 1
                            line.K += 1 / len(line.cells)
                            queue_del.append(car)
                    except:
                        pass

                Map.nodes[spawn_node].queue = [temp for temp in Map.nodes[spawn_node].queue if not (temp in queue_del) ]



    @staticmethod
    def comp():  # dt = 1 s

        CarDriver.assignCars()

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x == -1:
                continue

            line = car.getLines()[car.currentLine]
            try:
                gap = line.cells.index(1, car.x + 1) - car.x
                if gap == -1:
                    car.next_x = car.CompV(max(car.getRoad().max_velocity, len(line.cells) - car.x))
                else:
                    car.next_x = car.CompV(gap)
            except ValueError:
                car.next_x = car.CompV(max(car.getRoad().max_velocity, len(line.cells) - car.x))


        for car_index, car in enumerate(CarDriver.cars_array):



            if car.x == -1:
                continue

            line = car.getLines()[car.currentLine]
            line.cells[car.x] = 0
            line.K -= 1 / len(line.cells)
            if car.next_x >= len(line.cells):
                if car.wayProgress + 1 >= len(car.way):
                    # if the car ends his path
                    # he will change his path and change his delay
                    parking_node = Map.nodes[car.getRoad().end_node]

                    if parking_node.n_parking_places <= len(parking_node.queue):
                        line.K += 1 / len(line.cells)
                        line.cells[-1] = 1
                        car.next_x = len(line.cells) - 1
                    else:
                        car.next_x = -1
                        car.delay = random.randrange(DelayForCarLow, DelayForCarHigh)
                        if random.randrange(0, 10) <= ProbabilityOfEntertainment * 10:
                            entertainment_node = random.choice([i for i in Map.spawn_nodes if i != car.home_node and i != car.work_node])
                            way = GraphAlgorithms.A_Star(Map.nodes, parking_node.index, entertainment_node)
                        else:
                            if car.home_node != parking_node.index:
                                way = GraphAlgorithms.A_Star(Map.nodes, parking_node.index, car.home_node)
                            else:
                                way = GraphAlgorithms.A_Star(Map.nodes, parking_node.index, car.work_node)

                        for x in way:
                            car.addWayNode(x[0], x[1], x[2])

                        car.pos = (0, None)
                        parking_node.queue.append(car)

                    # del CarDriver.cars_array[car_index]
                    # del car
                    # line.K -= 1 / len(line.cells)
                    # continue

                else:
                    
                    # observing the next line, because car is going there
                    car.next_x -= len(line.cells)
                    old_line = car.currentLine
                    car.wayProgress += 1
                    line.K -= 1 / len(line.cells)
                    car.currentLine = random.randrange(len(car.getLines()))
                    line = car.getLines()[car.currentLine]

                    try:
                        gap = line.cells.index(1, 0)
                        if gap == -1:
                            car.next_x = min(car.next_x, car.CompV(min(car.getRoad().max_velocity, len(line.cells))))
                        else:
                            car.next_x = min(car.next_x, car.CompV(gap))
                    except ValueError:
                        car.next_x = min(car.next_x, car.CompV(min(car.getRoad().max_velocity, len(line.cells))))
                    
                    if car.next_x == 0:
                        car.wayProgress -= 1
                        car.currentLine = old_line
                        line = car.getLines()[car.currentLine]
                        car.next_x = len(line.cells) - 1
                    
                    line.K += 1 / len(line.cells)

            
            car.x = car.next_x
            try:
                if car.x != -1:
                    car.getLines()[car.currentLine].cells[car.x] = 1
                    line.K += 1 / len(line.cells)
            except:
                del CarDriver.cars_array[car_index]
                del car

    def __get_path(u, v):
        return GraphAlgorithms.dijkstra(Map.distance_matrix, u, v)
