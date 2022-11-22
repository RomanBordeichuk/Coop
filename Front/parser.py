import json
import math
from .constructor import Constructor

def decodeCars(message):

    data = json.loads(str(message))

    #html = ''

    # offset_x = min_cars(data['cars'], 0)
    # offset_y = min_cars(data['cars'], 1)

    # print(offset_x)
    #print(data['cars'])
    cars = data["cars"]
    # print(cars)        

    #html += Constructor.constructCars(cars)
    cars_array = json.dumps(Constructor.constructCars(cars))
    
    return cars_array

def decodeLights(data):
    
    lights_array = json.dumps(Constructor.constructLights(data))

    return lights_array

def decodeMap(data):
    html = ''
    # count = 0

    nodes = data['nodes']
    roads = data['roads']

    Constructor.setSystem(nodes, roads)
    html += Constructor.constructNodes()
    html += Constructor.constructRoads()

    return html