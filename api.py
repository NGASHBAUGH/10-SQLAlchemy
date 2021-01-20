#Import all items needed 
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import numpy as np
from sqlalchemy.sql.expression import func

# create engine
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#create an app activating flask 
app = Flask(__name__)

#create home page withlinks to all other routes 
@app.route("/")
def helloworld():
    #URL that tell the user the end points that are availible 
    return ("Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:  <br/>"
        f"To find the list of Stations: /stations <br/>"
        f"To find the precipitation by Date: /precipitation <br/>"
        f"To look at the date and tempurature of the most used station: /tobs <br/>"
        f"To look at the max, min, and average of all stations begining at a specified start date: /api/v1.0/start <br/>"
        f"To look at the max, min, and average of all stations begining at a specified start and end date: /api/v1.0/start/end <br/>"

)
        

#crete a station's name page 
@app.route("/stations")
def stations():
    station_names = session.query(Station.name).all()
    station_One_dimension = list(np.ravel(station_names))
    return jsonify(station_One_dimension)

#Return the JSON representation of query results to a dictionary using date as the key and prcp as the value.
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

# Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/tobs")
def tobs():
    Tresults = session.query( Measurement.date , Measurement.tobs ).filter(Measurement.station == "USC00519281").all()
    Tobs_Teresults = list(np.ravel(Tresults))
    return jsonify(Tobs_Teresults)

# JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range
@app.route("/api/v1.0/<start>")
def Start_Date(start):
    st_date = session.query( func.max(Measurement.tobs)  , func.min(Measurement.tobs) , func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_date = list(np.ravel(st_date))
    return jsonify(start_date)

# JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
@app.route("/api/v1.0/<start>/<end>")
def St_End(start, end):
    start_end_date = session.query( func.max(Measurement.tobs)  , func.min(Measurement.tobs) , func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    Start_End = list(np.ravel(start_end_date))   
    return jsonify(Start_End)


# run app
if __name__ == "__main__":
    app.run()

