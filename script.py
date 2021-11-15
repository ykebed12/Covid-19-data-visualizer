# import webbrowser
# import http.server
# import socketserver
from flask import Flask, redirect, url_for, render_template
from flask import current_app, g
from flask.cli import with_appcontext
from os import listdir
from os.path import isfile, join, isdir
import sqlite3
import json
import time
from datetime import datetime

#flask object
app = Flask(__name__)

#directory for database
DATABASE = './facility_cases.db'

#function to create db object
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    #return db object
    return db

#function counties data based on user input for date and state returns dictionary of county data
def get_counties_data(selected_date, state_name="California"):
    #cursor object for db acts as middle man between programmer and db
    cursor = get_db().cursor()

    

    # sql = f'''SELECT * FROM tb
    #                 (SELECT * FROM CountiesData
    #                     WHERE StateName="{state_name};"
    #                     ORDER BY ABS( JULIANDAY(Date)  - JULIANDAY("{selected_date}") )
    #                 ) as tb
    #             GROUP BY CountyName
    #             '''

    #sql script
    sql = f'SELECT * FROM CountiesData WHERE StateName="{state_name}" and Date="{selected_date}"'

    #fetch returns tuple
    counties_table = cursor.execute(sql).fetchall()

    #creating dictionary
    data_dict = dict()

    # Order in sql CountiesData table
    # `DataID` , `CountyName`,  `StateName`, `Cases` , `Deaths`,  `Date`,
    for _, county_name, _, cases, deaths, date in counties_table:
        data_dict[county_name] = {"Cases": cases,
                                  "Deaths": deaths,
                                  "Closest_Date": date}

    return data_dict

#returns the max and min date for counties for given state for data selector restriction
def max_min_date_county(state_name='California'):
    cursor = get_db().cursor()
    sql = f'SELECT MAX (Date) FROM CountiesData WHERE StateName="{state_name}"'
    max_date = datetime.fromisoformat(
        cursor.execute(sql).fetchone()[0]).strftime("%Y-%m-%d")
    sql = f'SELECT MIN (Date) FROM CountiesData WHERE StateName="{state_name}"'
    min_date = datetime.fromisoformat(
        cursor.execute(sql).fetchone()[0]).strftime("%Y-%m-%d")

    return max_date, min_date

#closing db connection after program is closed
#flask function to close application layer
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#flask function for home
@app.route('/')
def home():

    # Get only california facility data from sql database
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Facilities WHERE StateName="California"'
    facilities = list(cursor.execute(sql))

    # Get max and min date of county
    max_county_date, min_county_date = max_min_date_county(state_name='California')

    #returns website, facilities, max and min date to webpage.htl
    return render_template('webpage.html',
                           facilities=facilities,
                           max_county_date=max_county_date,
                           min_county_date=min_county_date)

#flask function whn user selecs a date
@app.route('/county_data/<selected_date>', methods=['GET', 'POST'])
def county_data_send(selected_date):

    county_data = get_counties_data(selected_date)
    return json.dumps(county_data)


if __name__ == "__main__":
    app.run()
