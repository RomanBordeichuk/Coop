import math
import json 

class Constructor:
    
    offset_x: int = 0
    offset_y: int = 0
    scale: int = 10
    nodes = None
    roads = None

    @staticmethod
    def min_map(data, index):
        off_min = math.inf

        for struct in data:
            off_min = min(struct[0][index], off_min)

        return off_min

    @staticmethod
    def setSystem(nodes, roads, reload=True):

        if(Constructor.nodes == None or reload):
            Constructor.nodes = nodes

        if(Constructor.roads == None or reload):
            Constructor.roads = roads
        
        Constructor.offset_x = Constructor.min_map(Constructor.nodes, 0)
        Constructor.offset_y = Constructor.min_map(Constructor.nodes, 1)

    @staticmethod
    def constructCars(cars):
        html = ''
        cars_array = dict()
        for car in cars:
            
            car_key = next(iter(car))
            position = car[car_key][0]
            x = (position[0][0]) + 11#+ (-1410 + 691.8 + 1)  #x
            y = (position[0][1]) + 14#+ (-510 + 472 + 27) #y
            rotate = (position[1]) #rotate
            speed = (position[2])
            road = car[car_key][1]
            color = car[car_key][2]
            iroad1 = road[0]  # === car.getRoad().index
            iroad2 = road[1]
            if iroad1 in Constructor.roads[iroad2]:
                x -= 7 * math.sin(rotate)
                y += 7 * math.cos(rotate)

                rotate *= 180 / math.pi
            cars_array[car_key] = [x, y, rotate, speed, iroad1, iroad2, color]
            #html += f'<div class="car_red" id="car_{car_key}" style="left: {x}px; top: {y}px; transform: rotate({rotate}deg);"> </div>'

        return cars_array

    @staticmethod
    def constructLights(lights):
        html = ''

        # list[list[id, sublights, self.array_roads, self.periods, self._is_first_open, self.counter] <- one light
        # sublights -> list[sublight] -> list[list[[x, y], angle, color]]
        
        
        #This implementation should be probable changed in the future to return json
        lights_array = dict()
        for light in lights:
            #html += f'<div class="light" id="light_{light[0]}">'
            lights_array[light[0]] = [light[0], "temp", light[3][0], light[3][1]] # di, sublights, periods
            sublights_array = []
            for sublight in light[1]:
                x = sublight[0][0] + 11
                y = sublight[0][1] + 14
                angle = sublight[1] * 180 / math.pi
                color = sublight[2]

                sublights_array.append([x, y, angle, color])
                #html += f'<div class="sublight" id="sublight_{light_index}" style="left: {x}px; top: {y}px; transform: rotate({angle}deg); background-color: {color}"> </div>'
            lights_array[light[0]][1] = sublights_array
                
            
            #html += '</div>'
        return lights_array

    @staticmethod
    def constructNodes():
        html = ''

        for index, node in enumerate(Constructor.nodes):
            x = (node[0][0] - Constructor.offset_x) * Constructor.scale
            y = (node[0][1] - Constructor.offset_y) * Constructor.scale
            node[0][0] = x
            node[0][1] = y

            html += f'<div class="main_circle" id="node_{index}"  onclick="get_light_editor({index})" style="left: {x}px; top: {y}px; "></div>'

        return html

    @staticmethod
    def constructRoads():
        html = ''
        road_index = 0

        for iroad1 in Constructor.roads.keys():
            for iroad2 in Constructor.roads[iroad1].keys():
                if len(Constructor.roads[iroad1][iroad2]) == 0: 
                    continue
                
                x1 = Constructor.nodes[int(iroad1)][0][0] + 18
                y1 = Constructor.nodes[int(iroad1)][0][1] + 18
                x2 = Constructor.nodes[int(iroad2)][0][0] + 18
                y2 = Constructor.nodes[int(iroad2)][0][1] + 18

                x = (x1 + x2) / 2
                y = (y1 + y2) / 2

                length = ((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2)) ** 0.5
                road_index = Constructor.roads[iroad1][iroad2][2]
                is_open = Constructor.roads[iroad1][iroad2][3]
                if iroad1 in Constructor.roads[iroad2]:
                    if is_open:
                        html += f'<div class="road" id="road_{Constructor.roads[iroad1][iroad2][2]}" style="left: {(x - (length / 2))}px; top: {(y - 12) - 2}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);" onclick="show_road({Constructor.roads[iroad1][iroad2][2]})"></div>'
                    else:
                        html += f'<div class="forbidden_road" id="road_{Constructor.roads[iroad1][iroad2][2]}" style="left: {(x - (length / 2))}px; top: {(y - 12) - 2}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);" onclick="show_road({Constructor.roads[iroad1][iroad2][2]})"></div>'

                else:
                    if is_open:
                        html += f'<div class="road_one_line" id="road_{Constructor.roads[iroad1][iroad2][2]}" style="left: {(x - (length / 2))}px; top: {(y - 6)}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);" onclick="show_road({Constructor.roads[iroad1][iroad2][2]})"></div>'
                    else:
                        html += f'<div class="forbidden_road_one_line" id="road_{Constructor.roads[iroad1][iroad2][2]}" style="left: {(x - (length / 2))}px; top: {(y - 6)}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);" onclick="show_road({Constructor.roads[iroad1][iroad2][2]})"></div>'


                road_index += 1

        return html