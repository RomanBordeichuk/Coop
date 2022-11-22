import time
from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from Back.Model.CarController import CarDriver
from Back.Model.MainController import Controller
from Back.Model.Util.MapController import Map
from Back.Model.LightsController import LightsController
from Front.parser import *
from Front.db import Settings
from Back.Model.DbController import getParams
from Back.Model.PortController import PortDriver
import os
import pathlib
from werkzeug import *
import json
# Hell

# Presets' content below

received_status = False

Map_html = None
Cars_html = None

static_folder = 'Front'

# Flask's content below
app = Flask(__name__, static_folder=(static_folder + '/static'), static_url_path='', template_folder=(static_folder + "/templates"))

UPLOAD_FOLDER = os.path.abspath('Front/uploads')
ALLOWED_EXTENSIONS = set(['osm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

html = ''

from flask_restful import reqparse

def parse_arg_from_requests(arg, **kwargs):
    parse = reqparse.RequestParser()
    parse.add_argument(arg, **kwargs)
    args = parse.parse_args()
    return args[arg]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    #map = parser.datamap()
    #data = parser.data()
    #return render_template('index.html', data=data, map=map)
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            value = request.form.get('value')

            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            Settings.changeParams(file_path, value)
            return render_template('settings.html')
    
    else:

        return render_template('settings.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/2d', methods=['GET', 'POST'])
def type1():

    data = getParams()
    #Controller.init(data[1], data[2])
    map_ = None # Controller.Map

    # data = PortDriver.getCarsIntoFile()
    cars_ = None # json.loads(data)


    #in order to make a table of cars, I will parse it here first
    #I will still provide cars_ to the html just in case
    #The same is true for lights
    cars_table = None # PortDriver.parse_cars(cars_)

    lights = None # PortDriver.getLightsIntoFile()
    

    lights_table = None #PortDriver.parse_lights(lights)

    return render_template('2d.html', map = html, map_ = map_, cars_ = cars_, lights = lights, cars_table=cars_table, lights_table=lights_table)

@app.route('/map', methods=['GET', 'POST'])
def info():

    global html

    if request.method == 'GET':
        operation = parse_arg_from_requests('operation')

        if operation == None:
            # print(request.form)
            return render_template('2d.html', data=html)

        

        if operation == "setMap":
            

            data = getParams()
            Controller.init(data[1], data[2])

        
            html = decodeMap(Controller.Map)
            # print(html)
            return html


        elif operation == "setCars":
            start_time = time.perf_counter()
            Controller.change()
            cars_json = decodeCars(PortDriver.getCarsIntoFile())
            lights_json = decodeLights(PortDriver.getLightsIntoFile())    
            end_time = time.perf_counter ()
            print(end_time - start_time, "seconds for loop of getting cars and lights")        
            return json.dumps({"cars" : cars_json, "lights" : lights_json})


        else:
            pass

@app.route('/util_ajax', methods=['POST'])
def util_ajax():
    operation = parse_arg_from_requests('operation')
    if operation == None:
        pass
    elif operation == "setRoadMaxVelocity":
        road_index = int(parse_arg_from_requests("road_index"))
        max_velocity = int(parse_arg_from_requests("max_velocity"))
        Map.roads[road_index].max_velocity = max_velocity

    elif operation == "getRoadMaxVelocity":
        road_index = int(parse_arg_from_requests("road_index"))
        
        return json.dumps({"max_velocity" : Map.roads[road_index].max_velocity})

    elif operation == "setRoadStatus":
        road_index = int(parse_arg_from_requests("road_index"))
        road_status = int(parse_arg_from_requests("road_status")) # It's Bool, false - closed, true - open
        Map.roads[road_index].is_open = road_status

    elif operation == "getAllFromRoad":
        road_index = int(parse_arg_from_requests("road_index"))

        road = Map.roads[road_index]
        road.Flow()

        return json.dumps({"density" : road.K, "flow": road.flow, "start_node": road.start_node, 
                           "end_node": road.end_node, "n_lines": road.n_lines, "max_velocity": road.max_velocity})  

    elif operation == "getCarPath":
        car_index = int(parse_arg_from_requests("car_index"))
        # print({"way":[i.road.index for i in CarDriver.cars_array[car_index].way]})
        return json.dumps({"way":[i.road.index for i in CarDriver.cars_array[car_index].way]})

@app.route('/3d')
def type2():

    data = getParams()
    Controller.init(data[1], data[2])
    map_ = Controller.Map

    data = PortDriver.getCarsIntoFile()
    cars_ = json.loads(data)

    lights = PortDriver.getLightsIntoFile()

    return render_template('3d.html', map = html, map_ = map_, cars_ = cars_, lights = lights)

@app.route('/editior', methods=['GET', 'POST'])
def editior():
    if request.method == 'POST':
        value = request.form.get('data')
        print(value)
        return redirect('/2d')

@app.route('/car_3d', methods=['GET', 'POST'])
def cars():
    if request.method == 'GET':
        data = getParams()
        Controller.init(data[1], data[2])
        Controller.change()

        cars = PortDriver.getCarsIntoFile3D()
        cars_ = json.loads(cars)

        func_string = ''

        for car in cars_['cars']:
            for key in car.keys():
                x = car[key][0][0][0]    
                y = car[key][0][0][1]

                #string += f'createCar({b[0][0]}, {b[0][1]}, {b[1]});'
                func_string += f'createCar({x}, {y});' # car longitude and latitude 
                
        return func_string


@app.route('/lights_editor', methods=['POST'])
def lights_editor():
    light_id = int(request.form.get("light_id"))
    new_red_period = int(request.form.get("red_period"))
    new_green_period = int(request.form.get("green_period"))
    LightsController.traffic_lights[light_id].periods = [new_red_period, new_green_period]
    
    return("", 204)

@app.route('/price')
def price():
    price = PortDriver.price_counter()
    return price

if __name__ == "__main__":
    app.run(debug=True)
 
 