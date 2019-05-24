import os
import pandas as pd
import numpy as np
import sqlalchemy
import dash
import dash_core_components as dcc
import dash_html_components as html
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
        limit(20).all()

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
        limit(20).all()
    df = pd.DataFrame(results, columns=['App_Name', 'Rating'])

    # Format the data for Plotly
    plot_trace = {
        "x": df["App_Name"].values.tolist(),
        "y": df["Rating"].values.tolist(),
        "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/App_Count")
def app_count_data():
    """Return app count by category"""
    stmt = db.session.query(Appsdata).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    #df = pd.read_csv(
    #    'googleplaystore.csv')

    #print("df:")
    #print(df)

    reduced_df = df.loc[: , ['Category' , 'Installs']]
    #print("reduced_df:")
    #print(reduced_df)

    reduced_df['Installs'] = reduced_df['Installs']
    grouped_reduced_df = reduced_df.groupby(['Category']).count()
   # print("grouped:")
    #print(list(grouped_reduced_df.index))

    category_list = list(grouped_reduced_df.index)
    installs_count = list(grouped_reduced_df['Installs'])

   # Format the data for Plotly
    plot_trace = {
        "x": category_list,
        "y": installs_count,
        "type": "bar"
        
    }
    return jsonify(plot_trace)

@app.route("/MyData")
def Mydata():
    """Return google playstore apps top 10"""

    stmt = db.session.query(Appsdata).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    
    return jsonify(df.to_dict())

   
if __name__ == '__main__':
    app.run(debug=True)
