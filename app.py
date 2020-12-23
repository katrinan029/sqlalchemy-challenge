from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base

# Database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing datbase into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the Database
session = Session(bind=engine)

# Design a query to retrieve the last 12 months of precipatation data and plot the results
# Query the first date
session.query(Measurement.date).order_by(Measurement.date.desc()).first()
last_date = dt.date(2017, 8, 23)
query_date = last_date - dt.timedelta(days=365)

# Perform a query to retrieve the date and precipation scores
app = Flask(__name__)

# Flask routes


@app.route("/")
def home():
    ret = '''
    <br/>
    Welcome to the Climate app. Below are the available routes.<br/><br/>
    Available routes: <br/>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>
    <a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
    <a href="/api/v1.0/start_date">/api/v1.0/start_date</a><br/>
    <a href="/api/v1.0/start_date/end_date">/api/v1.0/start_date/end_date</a>
    '''

    return(ret)


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(bind=engine)

    annual_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= last_date, Measurement.date >= query_date).\
        order_by(Measurement.date).all()

    session.close()

    # Convert query results into a dictionary using date as the key and prcp as the value
    date_prcp = []

    for date, prcp in annual_prcp:
        date_prcp_dict = {}
        date_prcp_dict[date] = prcp
        date_prcp.append(date_prcp_dict)

    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(bind=engine)
    stations = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # Return the JSON list of stations from the dataset
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(bind=engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    station_tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date <= last_date,
               Measurement.date >= query_date).all()

    session.close()

    # Return a JSON list of temperature observations(TOBS) for the previous year
    return jsonify(station_tobs)


@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):

    session = Session(bind=engine)

    all_dates = session.query(Measurement.date).all()
    found = False

    for date in all_dates:
        if start_date == date[0]:
            query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
            found = True

    if not found:
        return jsonify({"Enter in a valid date between 2010-01-01 and 2017-08-23": f"Date {start_date} not found."}), 404

    return jsonify(query)

    session.close()


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps2(start_date, end_date):

    session = Session(bind=engine)
    all_dates = session.query(Measurement.date).all()
    start_date_found = False
    end_date_found = False
    for date in all_dates:
        if date[0] == start_date:
            start_date_found = True
        if date[0] == end_date:
            end_date_found = True

    if start_date_found == True and end_date_found == True:
        query_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(
                Measurement.date <= end_date).all()
        return jsonify(query_results)

    else:
        return jsonify({"Enter in a valid date between 2010-01-01 and 2017-08-23": f"Date {start_date} or {end_date} not found."}), 404

    session.close()


if __name__ == '__main__':
    app.run(debug=True)
