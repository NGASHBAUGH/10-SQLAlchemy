from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import numpy as np


from sqlalchemy.sql.expression import func

# create engine
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def helloworld():
    #URL that tell the user the end points that are availible 
    return "Hello World"

@app.route("/stations")
def stations():
    station_names = session.query(Station.station).all()
    station_One_dimension = list(np.ravel(station_names))
    return jsonify(station_One_dimension)

@app.route("/precipitation")
def precip():
    Presults = session.query(Measurement.date , Measurement.prcp).all()
    session.close()
    Prcplist = []
    for date, prcp in Presults:
        prcp_dict = {}
        prcp_dict[date] = prcp
        Prcplist.append(prcp_dict)
    return jsonify(Prcplist)


@app.route("/tobs")
def tobs():
    Tresults = session.query(Measurement.station ,  Measurement.date , Measurement.tobs ).filter(Measurement.station == "USC00519281").all()
    Tobs_Teresults = list(np.ravel(Tresults))
    return jsonify(Tobs_Teresults)

@app.route("/api/v1.0/<start>")
def Start_Date(start):
    st_date = session.query( func.max(Measurement.tobs)  , func.min(Measurement.tobs) , func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_date = list(np.ravel(st_date))
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def St_End(start, end):
    start_end_date = session.query( func.max(Measurement.tobs)  , func.min(Measurement.tobs) , func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    Start_End = list(np.ravel(start_end_date))   
    return jsonify(Start_End)

if __name__ == "__main__":
    app.run()

