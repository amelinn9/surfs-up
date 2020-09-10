# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# import dependencies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask dependencies
from flask import Flask, jsonify

# set up the database engine for the Flask app
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create variable for each class so we can reference them
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to the database
session = Session(engine)

# set up/define the Flask app
app = Flask(__name__)


# define the welcome route
@app.route("/")

# create a welcome() function
def welcome():
    return (
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')


# create the precipitation analysis route
@app.route("/api/v1.0/precipitation")

# create the precipitation() function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


# create the stations analysis route
@app.route("/api/v1.0/stations")

# create the stations() function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# create the temp observations route
@app.route("/api/v1.0/tobs")

# create the temp_monthly() function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# create the starting and ending date routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create the stats() function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
