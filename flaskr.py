
from flask import Flask, request, render_template, send_from_directory
from flask.ext.bootstrap import Bootstrap
import json
import re

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

# see http://flask.pocoo.org/snippets/56/
#def crossdomain(origin=None, methods=None, headers=None,
#                max_age=21600, attach_to_all=True,
#                automatic_options=True):
#    if methods is not None:
#        methods = ', '.join(sorted(x.upper() for x in methods))
#    if headers is not None and not isinstance(headers, basestring):
#        headers = ', '.join(x.upper() for x in headers)
#    if not isinstance(origin, basestring):
#        origin = ', '.join(origin)
#    if isinstance(max_age, timedelta):
#        max_age = max_age.total_seconds()
#
#    def get_methods():
#        if methods is not None:
#            return methods
#
#        options_resp = current_app.make_default_options_response()
#        return options_resp.headers['allow']
#
#    def decorator(f):
#        def wrapped_function(*args, **kwargs):
#            if automatic_options and request.method == 'OPTIONS':
#                resp = current_app.make_default_options_response()
#            else:
#                resp = make_response(f(*args, **kwargs))
#            if not attach_to_all and request.method != 'OPTIONS':
#                return resp
#
#            h = resp.headers
#
#            h['Access-Control-Allow-Origin'] = origin
#            h['Access-Control-Allow-Methods'] = get_methods()
#            h['Access-Control-Max-Age'] = str(max_age)
#            if headers is not None:
#                h['Access-Control-Allow-Headers'] = headers
#            return resp
#
#        f.provide_automatic_options = False
#        return update_wrapper(wrapped_function, f)
#    return decorator

app = Flask(__name__)

bootstrap = Bootstrap(app)

# Set debug mode.
debug = False

# ================
# REST API function definitions
# ================

# Stations
# =========
# Query:    GET /stations/all: lat, long, radius
# Response: array of station_id, lat, lon, zone_id, location tuples
@app.route('/REST/1.0/stations/all/<float:lat>/<float:lon>/<float:rad>')
#@crossdomain(origin='*')
def all_stations_in_rad(lat, lon, rad):
    return all_stations()
# This is just temporary so we have something to show.
@app.route('/REST/1.0/stations/all')
#@crossdomain(origin='*')
def all_stations():
    db = open('data/stations.json','r')
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    GET /stations/info: station_id
# Response: # bikes available, # of docks, location, fixed price, zone_id
@app.route('/REST/1.0/stations/info/<int:station_id>')
def stations_info(station_id):
    s = 'data/station_' + str(station_id) + '.json'
    print s
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    POST /stations/reserve: station_id, rider_id
# Response: time, dock_id, bike_id
@app.route('/REST/1.0/stations/reserve', methods=['POST'])
def reserve_station():
    # placeholder
    return '{}'

# Riders
# ========
# Query:    GET /riders/info: rider_id
# Response: f_name, l_name
@app.route('/REST/1.0/riders/info/<int:rider_id>')
def riders_info(rider_id):
    s = 'data/rider_' + str(rider_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    GET /riders/favorites/info: riderid
# Response: array of stationid, address
@app.route('/REST/1.0/riders/favorites/info/<int:rider_id>')
def favorite_info(rider_id):
    s = 'data/favorite_' + str(rider_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    POST /riders/favorites/add: stationid
# Response: success or failure code
@app.route('/REST/1.0/riders/favorites/add', methods=['POST'])
def add_favorite():
    # placeholder
    return '{}'

# Query:    POST /riders/favorites/remove: stationid
# Response: success or failure code
@app.route('/REST/1.0/riders/favorites/remove', methods=['POST'])
def remove_favorite():
    # placeholder
    return '{}'

# Query:    GET /riders/history: riderid
# Response: array of tripid, time
@app.route('/REST/1.0/riders/history/<int:rider_id>')
def rider_history(rider_id):
    s = 'data/history_' + str(rider_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Bikes
# ========
# Query:    GET /bikes/active: lat, long, radius
# Response: array of bike_id, lat, long tuples
@app.route('/REST/1.0/bikes/active/<float:lat>/<float:lon>/<float:rad>')
def active_bikes_in_rad(lat, lon, rad):
    return active_bikes()
# This is just temporary so we have something to show.
@app.route('/REST/1.0/bikes/active')
def active_bikes():
    db = open('data/bikes.json','r')
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    GET /bikes/info: bike_id
# Response: lat, long, distance biked, total time, array of reports
@app.route('/REST/1.0/bikes/info/<int:bike_id>')
def bike_info(bike_id):
    s = 'data/bike_' + str(bike_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    POST /bikes/checkout: bike_id, rider_id
# Response: trip_id
@app.route('/REST/1.0/bikes/checkout', methods=['POST'])
def checkout_bike():
    # placeholder
    return '{}'

# Query:    POST /bikes/checkin: bike_id, rider_id, station_id, trip_id
# Response: success or failure code
@app.route('/REST/1.0/bikes/checkin', methods=['POST'])
def checkin_bike():
    # placeholder
    return '{}'

# Query:    POST /bikes/report: bike_id, rider_id, array of bike status info
# Response: success or failure code
@app.route('/REST/1.0/bikes/report', methods=['POST'])
def report_bike_damage():
    # placeholder
    return '{}'

# Trips
# ========
# Query:    GET /trips/info: trip_id
# Response: start station_id, end station_id, date, array of lat, long
@app.route('/REST/1.0/trips/info/<int:trip_id>')
def trip_info(trip_id):
    s = 'data/trip_' + str(trip_id) + '.json'
    try:
        db = open(s,'r')
    except IOError:
        return '{}', 404
    data = json.load(db)
    return json.dumps(data, ensure_ascii=True)

# Query:    POST /trips/point: trip_id, lat, long
# Response: success or failure code
# For sending current location to db
@app.route('/REST/1.0/trips/point', methods=['POST'])
def add_trip_point():
    # placeholder
    return '{}'

# ================
# Main app function definitions
# ================

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

@app.route('/javascript/<path:path>', methods=['GET','OPTIONS'])
def js_proxy(path):
    return send_from_directory(app.root_path + '/javascript/', path)

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
        app.run(host='127.0.0.1', port=8081, debug=True)
    else:
        app.run(host='0.0.0.0', port=8081, debug=True)

