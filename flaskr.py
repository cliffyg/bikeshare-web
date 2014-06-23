
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
import json
import re

app = Flask(__name__)

bootstrap = Bootstrap(app)

# Set debug mode.
debug = False

# REST API function definitions

# Stations
@app.route('/REST/1.0/stations/all/')
def all_stations():
    db = open('data/stations.json','r')
    stations = json.load(db)
    return json.dumps(stations, ensure_ascii=True)

@app.route('/REST/1.0/stations/all/<float:lat>/<float:lon>/<float:rad>')
def all_stations_in_rad(lat, lon, rad):
    return all_stations()

@app.route('/REST/1.0/stations/info/<int:station_id>')
def stations_info(station_id):
    s = 'data/station_' + str(station_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    stations = json.load(db)
    return json.dumps(stations, ensure_ascii=True)

# Riders

# Bikes

# Trips


@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    if re.match('/REST',request.path):
        return '{}', 404
    else:
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    if re.match('/REST',request.path):
        return '{}', 500
    else:
        return render_template('500.html'), 500

if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False)

