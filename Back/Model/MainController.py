from .CarController import CarDriver
from .PortController import PortDriver
from .LightsController import LightsController
from .Util.MapController import Map
from .Util.Consts import *
# from .MessageController import ServerRabbit
from base64 import b64decode
from json import loads


class Controller:

    Map = {}
    Cars = {}

    @staticmethod
    def setMap(Name):
        # Rabbit.Init()
        # clearQueue("cars")
        # clearQueue("map")

        if ',' in Name:
            PortDriver.setMapByName(Name)
        else:
            PortDriver.setMapFromFile(Name)


    @staticmethod
    def init(NameMap, n_cars):
        NCars = n_cars
        Controller.Map = {}
        Controller.Cars = {}
        Controller.setMap(NameMap)
        Controller.Map = PortDriver.getMapIntoFile()
        Map.init(n_cars)

        CarDriver.init()
        LightsController.init()

    @staticmethod
    def change():

        CarDriver.comp()
        LightsController.comp()
        # PortDriver.getCarsIntoFile()




    @staticmethod
    def setMapJson():
        PortDriver.setMapFromFile(NameMapFile)