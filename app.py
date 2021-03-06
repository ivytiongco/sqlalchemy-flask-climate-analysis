import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/passengers<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including the date and prcp"""
    # Query measurement data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_measurements = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query dates and tobs of most active station for last yr of data
    # Most active station and dates of last yr of data was found in jupyter notebook analysis
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)
  
@app.route("/api/v1.0/<start>")
def start_temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the min temp, avg temp, max temp for given start date 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_temps = list(np.ravel(results))

    return jsonify(all_start_temps)
        

@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for the min temp, avg temp, max temp for given start date 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_end_temps = list(np.ravel(results))

    return jsonify(all_start_end_temps)

if __name__ == '__main__':
    app.run(debug=True)
