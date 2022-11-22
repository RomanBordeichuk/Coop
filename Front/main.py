from flask import *
from .parser import *
from .db import *
from .rabbitmq import *
import os
from werkzeug import *

# Presets' content below

received_status = False

Rabbit = ClientRabbit()

Map_html = None
Cars_html = None

# Flask's content below
app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = set(['osm'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

            db.changeParams(file_path, value)
            return render_template('settings.html')
    
    else:

        return render_template('settings.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/2d', methods=['GET', 'POST'])
def type1():
    # map = parser.datamap()
    # data = parser.data()

    global received_status

    received_status = False
    html = ''

    if request.method == 'GET':
        operation = request.json['operation']
        if operation == "setMap":
            Rabbit.sendData('setMap', 'control')
            while not received_status:
                pass

            html = Map_html


        if operation == "setCars":
            Rabbit.sendData('setCars', 'control')
            while not received_status:
                pass

            html = Cars_html
            
            
    
    received_status = False

    return render_template('2d.html', data = html)

@app.route('/3d')
def type2():
    return render_template('3d.html')

def runServer():
    app.run(debug=True)
    Rabbit.startConsuming()

