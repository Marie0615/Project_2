import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup v2
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/playstore.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Appsdata = Base.classes.storedata
user_reviews = Base.classes.user_reviews



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/Top_Apps")
def top_apps_data():
    """Return google playstore apps top 10"""

    # Query for the top 10 apps data
    results = db.session.query(Appsdata.App_Name, Appsdata.Installs).\
        order_by(Appsdata.Installs.desc()).\
        limit(10).all()

    # Create lists from the query results
    apps_category = [result[0] for result in results]
    apps_installs = [result[1] for result in results]

    # Generate the plot trace
    trace = {
        "x": apps_category,
        "y": apps_installs,
        "type": "bar"
    }
    return jsonify(trace)

@app.route("/App_Name")
def app_name_data():
    """Return ratings and app name"""

    # Query for the top 10 app rating
    results = db.session.query(Appsdata.App_Name, Appsdata.Rating).\
        order_by(Appsdata.Rating.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['App_Name', 'Rating'])

    # Format the data for Plotly
    plot_trace = {
        "x": df["App_Name"].values.tolist(),
        "y": df["Rating"].values.tolist(),
        "type": "bar"
    }
    return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
