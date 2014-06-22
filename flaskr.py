
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
import json

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
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=False)

