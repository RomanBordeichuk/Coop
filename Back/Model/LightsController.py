from random import randrange
from .Util.TrafficLightInstance import TrafficLight
from .Util.MapController import Map
from .Util.Consts import StartPeriodLow, StartPeriodHigh

class LightsController:

    #traffic_lights : dict[TrafficLight] = []
    traffic_lights = dict()

    @staticmethod
    def init():
        #traffic light id will be equal to the light_id to make web function of getting light id much simpler.
        # By the way, I want to make make everything in dictionaries, we should make cars the same way, wee are iterating over them with for each loop every time, and it is I guess O(n), but in order to change them 
        # efficiently we will use maps and change them in O(log(n))
        for node_index, node in enumerate(Map.nodes):
            if node.type != 'intersect' or len(node.end_roads) < 3:
                continue

            
            LightsController.traffic_lights[node_index] = (TrafficLight(node_index, node.end_roads,
                                                    [randrange(StartPeriodLow, StartPeriodHigh),
                                                     randrange(StartPeriodLow, StartPeriodHigh)],
                                                    node_index))


    @staticmethod
    def comp():
        for light in LightsController.traffic_lights.values():
            light.Change()


    @staticmethod
    def getLigths():
        lights = []

        for light in LightsController.traffic_lights.values():
            lights.append(light.getAttributes())


        return lights
            