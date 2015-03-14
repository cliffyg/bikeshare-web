import syslog
from flask import Flask, request, render_template, send_from_directory, jsonify
from flask.ext.bootstrap import Bootstrap
import re
import urllib2

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import sstoreclient

app = Flask(__name__)

bootstrap = Bootstrap(app)

# Set debug mode.
debug = False

# ================
# REST API function definitions
# ================

# Users
# ========

# Get all users
# ---------
# Verb:     GET
# Route:    /REST/1.0/users/all
# Response: { "users": [{<string:CREDIT_CARD>, <int:MEMBERSHIP_STATUS>,
#                        <int:USER_ID>, <string:USER_NAME>}, ...] }
@app.route('/REST/1.0/users/all')
def all_users():
    db = sstoreclient.sstoreclient()
    proc = 'Users'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"users" : data['data']})

# Get single user
# ---------
# Verb:     GET
# Route:    /REST/1.0/users/info/<user_name>
# Response: {<>, <>, <>}
@app.route('/REST/1.0/users/info/<user_name>')
def user_info(user_name):
    db = sstoreclient.sstoreclient()
    proc = 'FindUser'
    args = [urllib2.unquote(user_name)]
    print args
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        userdata = data['data']
        if len(userdata) > 0:
            return jsonify(userdata[0])
        else:
            return '{}', 404
# Logins
# ========

# User registration
# ---------
# Verb:      POST
# Route:     /REST/1.0/login/signup
# Form data: <string:first_name>,<string:last_name>
# Response:  {<int:USER_ID>}
@app.route('/REST/1.0/login/signup', methods=['POST'])
def user_signup():
    db = sstoreclient.sstoreclient()
    proc = 'SignUpName'
    fname = request.form['first_name']
    lname = request.form['last_name']
    args = [fname,lname]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        users = data['data']
        return jsonify(users[0])

# User login
# ---------
# Verb:      POST
# Route:     /REST/1.0/login/check
# Form data: <string:user_name>
# Response:  {<int:USER_ID>}
@app.route('/REST/1.0/login/check', methods=['POST'])
def check_login():
    db = sstoreclient.sstoreclient()
    proc = 'FindUser'
    args = [request.form['user_name']]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        # TODO: Figure out what makes sense in the schema to use as a unique
        # token for login purposes.
        users = data['data']
        if len(users) > 0:
            return jsonify(subdict(data['data'][0],'USER_ID'))
        else:
            return '{}', 404

# Stations
# =========

# Get nearby stations
# ---------
# Verb:     GET
# Route:    /REST/1.0/stations/all
# Response: { "stations": [{<int:STATION_ID>, <string:STATION_NAME>,
#                           <int:LATITUDE>, <int:LONGITUDE>,
#                           <string:STREET_ADDRESS>}, ...] }
@app.route('/REST/1.0/stations/all')
def all_stations():
    db = sstoreclient.sstoreclient()
    proc = 'Stations'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"stations" : data['data']})

# Verb:     GET
# Route:    /REST/1.0/stations/all/<float:lat>/<float:lon>/<float:rad>
# Response: [{<int:STATION_ID>, <string:STATION_NAME>, <int:LATITUDE>,
#             <int:LONGITUDE>, <string:STREET_ADDRESS>}, ...]
@app.route('/REST/1.0/stations/all/<float:lat>/<float:lon>/<float:rad>')
def all_stations_in_rad(lat, lon, rad):
    return all_stations()


'''
# Get Portland stations
# ---------
# Verb:     GET
# Route:    /REST/1.0/stations/PDX
# Response: { "PDX_stations": [{<int:STATION_ID>, <string:STATION_NAME>,
#                               <int:LATITUDE>, <int:LONGITUDE>,
#                               <string:STREET_ADDRESS>}, ...] }
@app.route('/REST/1.0/stations/PDX')
def PDX_stations():
    db = sstoreclient.sstoreclient()
    proc = 'PDXStations'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"pdxstations" : data['data']})

# Get MIT stations
# ---------
# Verb:     GET
# Route:    /REST/1.0/stations/MIT
# Response: { "MIT": [{<int:STATION_ID>, <string:STATION_NAME>,
#                               <int:LATITUDE>, <int:LONGITUDE>,
#                               <string:STREET_ADDRESS>}, ...] }
@app.route('/REST/1.0/stations/MIT')
def MIT_stations():
    db = sstoreclient.sstoreclient()
    proc = 'MITStations'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"mitstations" : data['data']})       
'''

# Get stations from a city
# ---------
# Verb:     GET
# Route:    /REST/1.0/stations/<string:city>
# Response: { "stations": [{<int:STATION_ID>, <string:STATION_NAME>,
#                               <int:LATITUDE>, <int:LONGITUDE>,
#                               <string:STREET_ADDRESS>}, ...] }
@app.route('/REST/1.0/stations/<string:city>')
def Stations_in_City(city):
    db = sstoreclient.sstoreclient()
    proc = 'GetStationsInCity'
    args = [city]
    try:
        data = db.call_proc(proc, args)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        log_procerr(proc,str(data['error']))
        return '{}', 500
    else:
        return jsonify({"stations" : data['data']})       

# Get individual station info
# ---------
# Verb:     GET
# Route:    /REST/1.0/stations/info/<int:station_id>
# Response: {<int:STATION_ID>,<string:STATION_NAME>,<string:STREET_ADDRESS>,
#            <int:LATITUDE>,<int:LONGITUDE>,<int:CURRENT_BIKES>,
#            <int:CURRENT_DOCKS>,<int:CURRENT_DISCOUNT>
@app.route('/REST/1.0/stations/info/<int:station_id>')
def stations_info(station_id):
    db = sstoreclient.sstoreclient()
    proc = 'GetStationStatus'
    args = [station_id]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        stations = data['data']
        if len(stations) > 0:
            return jsonify(stations[0])
        else:
            return '{}', 404


# Bikes
# ========

# Get all bikes
# ---------
# Verb:     GET
# Route:    /REST/1.0/bikes/all
# Response: { "bikes": [{<int:BIKE_ID>, <int:USER_ID>, <int:CURRENT_STATUS>,
#                        <int:STATION_ID>}, ...] }
@app.route('/REST/1.0/bikes/all')
def all_bikes():
    db = sstoreclient.sstoreclient()
    proc = 'Bikes'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"bikes" : data['data']})

# Get current bike positions
# ---------
# Verb:     GET
# Route:    /REST/1.0/bikes/active
# Response: [ {<int:USER_ID>,<float:LATITUDE>,<float:LONGITUDE>}, ... ]
@app.route('/REST/1.0/bikes/active')
def active_bikes():
    db = sstoreclient.sstoreclient()
    proc = 'UserLocations'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        return jsonify({"bikes" : data['data']})
# Verb:     GET
# Route:    /REST/1.0/bikes/active/<float:lat>/<float:lon>/<float:rad>
# Response: [ {<int:USER_ID>,<float:LATITUDE>,<float:LONGITUDE>}, ... ]
@app.route('/REST/1.0/bikes/active/<float:lat>/<float:lon>/<float:rad>')
def active_bikes_in_rad(lat, lon, rad):
    return active_bikes()

# Get individual bike info
# ---------
# Verb:     GET
# Route:    /REST/1.0/bikes/info/<int:user_id>
# Response: {<int:USER_ID>,<float:LATITUDE>,<float:LONGITUDE>}
@app.route('/REST/1.0/bikes/info/<int:user_id>')
def bike_info(user_id):
    db = sstoreclient.sstoreclient()
    proc = 'GetBikeStatus'
    args = [user_id]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '{}', 500
    # Success case
    else:
        bikedata = data['data']
        if len(bikedata) > 0:
            return jsonify(bikedata[0])
        else:
            return '{}', 404

# Checkout bike
# ---------
# Verb:      POST
# Route:     /REST/1.0/bikes/checkout
# Form data: <int:station_id>,<int:user_id>
# Response:  Success (200)
#            Failure (401) - User does not exist
#            Failure (403) - User already has a bike checked out
#            Failure (503) - No bikes available at station
@app.route('/REST/1.0/bikes/checkout', methods=['POST'])
def checkout_bike():
    db = sstoreclient.sstoreclient()
    proc = 'CheckoutBike'
    user = int(request.form['user_id'])
    station = int(request.form['station_id'])
    args = [user, station]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        nouserstr = 'Rider: ' + str(user) + ' does not exist'
        alreadystr = 'Rider: ' + str(user) + ' already has a bike checked out'
        nobikestr = 'Rider: ' + str(user) + ' was unable to checkout a bike'
        if re.search(nouserstr,data['error']):
            return '{}', 401 # Unauthorized
        elif re.search(alreadystr,data['error']):
            return '{}', 403 # Forbidden
        elif re.search(nobikestr,data['error']):
            return '{}', 503 # Service Unavailable
        else:
            log_procerr(proc,str(data['error']))
            return '{}', 500
    # Success case
    else:
        return jsonify(data['data'])

# Checkin bike
# ---------
# Verb:      POST
# Route:     /REST/1.0/bikes/checkin
# Form data: <int:station_id>,<int:user_id>
# Response:  Success (200)
#            Failure (401) - User does not exist
#            Failure (403) - User does not have a bike to checkin
#            Failure (503) - No docks available at station
@app.route('/REST/1.0/bikes/checkin', methods=['POST'])
def checkin_bike():
    db = sstoreclient.sstoreclient()
    proc = 'CheckinBike'
    user = int(request.form['user_id'])
    station = int(request.form['station_id'])
    args = [user, station]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc,args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        nouserstr = 'Rider: ' + str(user) + ' does not exist'
        nobikestr = 'Rider ' + str(user) + ' does not have a bike checked out'
        nodockstr = 'Rider: ' + str(user) + ' was unable to checkin a bike'
        if re.search(nouserstr,data['error']):
            return '{}', 401 # Unauthorized
        elif re.search(nobikestr,data['error']):
            return '{}', 403 # Forbidden
        elif re.search(nodockstr,data['error']):
            return '{}', 503 # Service Unavailable
        else:
            log_procerr(proc,str(data['error']))
            return '{}', 500
    # Success case
    else:
        return jsonify(data['data'])

# Send recent bike positional data
# ---------
# Verb:      POST
# Route:     /REST/1.0/bikes/pos
# Form data: <int:user_id>,<float:lat>,<float:lon>
# Response:  Success (200)
#            Failure (401) - User does not exist
@app.route('/REST/1.0/bikes/pos', methods=['POST'])
def send_bike_position():
    db = sstoreclient.sstoreclient()
    proc = 'RideBike'
    user = int(request.form['user_id'])
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    args = [user, lat, lon]
    try:
        # Get data from S-Store.
        data = db.call_proc(proc, args)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc, str(e)) 
        return '{}', 500
    if not data['success']:
        # DB procedure execution failed.
        nouserstr = 'Rider: ' + str(user) + ' does not exist'
        nobikestr = 'Rider: ' + str(user) + ' does not have a bike checked out'
        if re.search(nouserstr,data['error']):
            return '{}', 401 # Unauthorized
        elif re.search(nobikestr,data['error']):
            return '{}', 403 # Forbidden
        else:
            log_procerr(proc,str(data['error']))
            return '{}', 500
    # Success case
    else:
        return jsonify(data['data'])
# Anomaly function
# ========

# Get anomalies
# --------
# Verb:     GET
# Route:    /REST/1.0/anomalies
# Response {anomalies: [{<int:USER_ID>, <int:STATUS>}, ...]}
@app.route('/REST/1.0/anomalies')
def get_anomalies():
    db = sstoreclient.sstoreclient()
    proc = 'GetAnomalies'
    try:
        data = db.call_proc(proc)
    except Exception as e:
        log_procerr(proc,str(e))
        return '{}', 500
    return jsonify({"anomalies" : data['data']})

# Other API functions
# ========

# Get general statistics
# ---------
# Verb:     GET
# Route:    /REST/1.0/stats
# Response: {<int:BIKES>,<int:ACTIVE_BIKES>,<int:STATIONS>,<int:PORSTATIONS>,
#            <int:MITSTATIONS>,<int:USERS>,<int:BIKES_PER_STATION}
@app.route('/REST/1.0/stats')
def get_stats():
    stats = dict()
    #stats['BIKES'], stats['ACTIVE_BIKES'] = get_bikestats()
    #stats['ACTIVE_BIKES'] = get_bikestats()
    city_bikestats = get_bikesincitiesstats()
    stats['PORBIKES'] = city_bikestats[0]
    stats['POR_ACTIVE_BIKES'] = city_bikestats[1]
    stats['MITBIKES'] = city_bikestats[2]
    stats['MIT_ACTIVE_BIKES'] = city_bikestats[3]
    stats['STATIONS'] = get_stationstats()
    city_stationstats = get_multiplestationstats()
    stats['PORSTATIONS'] = city_stationstats[0]
    stats['MITSTATIONS'] = city_stationstats[1]
    stats['USERS'] = get_userstats()
    stats['BIKES_PER_STATION'] = stats['PORBIKES'] // stats['STATIONS']
    log_procerr(str(stats), 'say what')
    return jsonify(stats)

# Get statistics about bikes.
def get_bikestats():
    db = sstoreclient.sstoreclient()
    proc = 'Bikes'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '?'
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '?'
    # Success case
    else:
        bikes = data['data']
        active = 0
        for bike in bikes:
            if bike['CURRENT_STATUS'] == 2:
                active = active + 1
        return len(data['data']), active

# Get statistics about bikes in different cities
def get_bikesincitiesstats():
    db = sstoreclient.sstoreclient()
    proc = 'Bikes'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '?'
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '?'
    # Success case
    else:
        bikes = data['data']
        por_active = 0
        mit_active = 0
        por = []
        mit = []
        for bike in bikes:
            if bike['CITY'] == 'PDX':
                por += [bike['CITY']]
                if bike['CURRENT_STATUS'] == 2:
                    por_active += 1
            if bike['CITY'] == 'MIT':
                mit += [bike['CITY']]
                if bike['CURRENT_STATUS'] == 2:
                    mit_active += 1
        return len(por), por_active, len(mit), mit_active

# Get statistics about stations.
def get_stationstats():
    db = sstoreclient.sstoreclient()
    proc = 'Stations'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '?'
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '?'
    # Success case
    else:
        return len(data['data'])

def get_multiplestationstats():
    db = sstoreclient.sstoreclient()
    proc = 'Stations'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,st(e))
        return '?'
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '?'
    # Success case
    else:
        por = []
        mit = []
        for i in data['data']:
            if i['CITY'] == "PDX":
                por += [i['CITY']]
            elif i['CITY'] == "MIT":
                mit += [i['CITY']]
        return len(por), len(mit)

# Get statistics about users.
def get_userstats():
    db = sstoreclient.sstoreclient()
    proc = 'Users'
    try:
        # Get data from S-Store.
        data = db.call_proc(proc)
    # Failure cases
    except Exception as e:
        # Client failed to connect to or get data from S-Store.
        log_procerr(proc,str(e))
        return '?'
    if not data['success']:
        # DB procedure execution failed.
        log_procerr(proc,str(data['error']))
        return '?'
    # Success case
    else:
        return len(data['data'])

# Helper function. Extracts and returns only the set of key/value pairs that
# we want from a given dict.
def subdict(d, keys):
    d2 = dict()
    for k, v in d.iteritems():
        if k in keys:
            d2[k] = v
    return d2

def log_procerr(proc = '', msg = ''):
    err = 'Exception encountered when calling S-Store procedure "'
    err += proc + '": ' + msg
    syslog.syslog(syslog.LOG_ERR, err)
    return


@app.errorhandler(404)
def page_not_found(e):
    return '{}', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '{}', 500

if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=8081, debug=True)
    else:
        app.run(host='0.0.0.0', port=8081, debug=True)

