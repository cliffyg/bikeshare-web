import syslog
from flask import Flask, request, render_template, send_from_directory
from flask.ext.bootstrap import Bootstrap
import json
import re
import syslog
import urllib2
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import sstoreclient
import requests

app = Flask(__name__)
app.config.setdefault('BOOTSTRAP_SERVE_LOCAL',True)
bootstrap = Bootstrap(app)

# Set debug mode.
debug = False

apiurl = 'http://api.bikeshare.cs.pdx.edu'

# ================
# Main app function definitions
# ================

# This is a GET route to display the "view all stations" page
@app.route('/stations')
def view_all_stations():
    apiroute = '/REST/1.0/stations/all'
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        return render_template('stations.html',stations_list=data['stations'],
            list_len=len(data))
    else:
        return render_template('500.html')

# This is a GET route to display the "view all bikes" page
@app.route('/bikes')
def view_all_bikes():
    apiroute = '/REST/1.0/bikes/all'
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        return render_template('bikes.html', bikes=data['bikes'])
    else:
        return render_template('500.html')

# This is a GET route to display the "view all riders" page
@app.route('/users')
def view_all_riders():
    apiroute = '/REST/1.0/users/all'
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        return render_template('users.html', users=data['users'])
    else:
        return render_template('500.html')

# This is a GET route to display the landing page of bikeshare
@app.route('/')
def home():
    apiroute = '/REST/1.0/stats'
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        return render_template('index.html', bikes=data['BIKES'],
            active_bikes = data['ACTIVE_BIKES'], stations=data['STATIONS'],
            users=data['USERS'], bikes_per_station=data['BIKES_PER_STATION'])
    else:
        return render_template('index.html')

# This is a GET route to display a single bike page of a given name
@app.route('/bike/<int:bike_id>')
def view_bike(bike_id):
    apiroute = '/REST/1.0/bikes/info/' + str(bike_id)
    print apiurl + apiroute
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        print data
        return render_template('bike.html',bike_id=bike_id, 
            user_id=data['USER_ID'], lat=data['LATITUDE'],
            lon=data['LONGITUDE'])
    else:
        return render_template('500.html')

# This is a GET route to display a single station page of a given name
@app.route('/station/<int:station_id>')
def view_station(station_id):
    apiroute = '/REST/1.0/stations/info/' + str(station_id)
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json()
        return render_template('station.html',station_id=station_id,
            name=data['STATION_NAME'],addr=data['STREET_ADDRESS'],
            lat=data['LATITUDE'],lon=data['LONGITUDE'],
            num_bikes=data['CURRENT_BIKES'],num_docks=data['CURRENT_DOCKS'],
            discount=data['CURRENT_DISCOUNT'])
    else:
        return render_template('500.html')

# This is a GET route to display a single user page of a given name
@app.route('/user/<user_name>')
def view_user(user_name):
    apiroute = '/REST/1.0/users/info/' + user_name
    r = requests.get(apiurl + apiroute)
    if r.status_code == 200:
        data = r.json ()
        return render_template('user.html', user=data)
    else:
        return render_template('500.html')

@app.route('/javascript/<path:path>', methods=['GET','OPTIONS'])
def js_proxy(path):
    return send_from_directory(app.root_path + '/javascript/', path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=8081, debug=True)
    else:
        app.run(host='0.0.0.0', port=8081, debug=True)

