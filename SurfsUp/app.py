import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


import datetime as dt
import numpy as np
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement

station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
############################################
#Year Ago
year_ago = '2016-08-23'
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start - start date example date 2016-09-23<br/>"
        f"/api/v1.0/start/end - start and end date example 2016-09-23/2017-03-16<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
    precip = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).group_by(measurement.date).all()
    precipt = []  
    for dater, precp in precip:
        precip_dict = {}
        precip_dict["date"] = dater
        precip_dict["prcp"] = precp
        precipt.append(precip_dict)

    return jsonify(precipt)

 
@app.route("/api/v1.0/stations")
def stationing():
    st = session.query(station).all()
    stationer = []  
    for sta in st:
        stationn = {}
        stationn["station"] = sta.station
        stationer.append(stationn)
    return jsonify(stationer)


@app.route("/api/v1.0/tobs")
def tobs():
    tob = session.query(measurement.date, measurement.station, measurement.tobs).filter(measurement.date >= year_ago).all()
    tobber = []
    for t in tob:
        tobb = {}
        tobb["date"] = t.date
        tobb["station"] = t.station
        tobb["tobs"] = t.tobs
        tobber.append(tobb)
    return jsonify(tobber)

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    rcalcs = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= date).all()
    dictt = []
    ls = {}
    ls["min"]=rcalcs[0][0]
    ls["max"]= rcalcs[0][1]
    ls["avg"]= rcalcs[0][2]
    dictt.append(ls)         
    return jsonify(dictt)

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    rcalcs = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    dictt = []
    ls = {}
    ls["min"]=rcalcs[0][0]
    ls["max"]= rcalcs[0][1]
    ls["avg"]= rcalcs[0][2]
    dictt.append(ls)         
    return jsonify(dictt)

if __name__ == '__main__':
    app.run(debug=True)

