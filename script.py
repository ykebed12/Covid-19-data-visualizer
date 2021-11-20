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

# flask object
app = Flask(__name__)

# directory for database
DATABASE = './facility_cases.db'

# function to create db object


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    # return db object
    return db

# function counties data based on user input for date and state
# that returns a dictionary of county data


def get_counties_data(selected_date, state_name="California"):
    # cursor object for db acts as middle man between programmer and db
    cursor = get_db().cursor()

    # sql script to get nearest date data point
    sql = f'''SELECT * 
                FROM (
                    SELECT ABS(JULIANDAY(Date(Date)) - JULIANDAY("{selected_date}")) as nearestDate,
                                    CountyName,
                                    Date,
                                    Cases,
                                    Deaths
                    FROM CountiesData
                    WHERE StateName="{state_name}"
                    ORDER BY nearestDate
                )
            GROUP BY CountyName'''

    # fetch returns tuple
    counties_table = cursor.execute(sql).fetchall()

    # creating dictionary
    data_dict = dict()

    # Order output of table
    # nearestDate, county_name, data, cases deate,
    for _, county_name, date, cases, deaths in counties_table:
        data_dict[county_name] = {"Cases": cases,
                                  "Deaths": deaths,
                                  "Closest_Date": date}

    return data_dict


def get_facilities_data(selected_date, state_name="California"):
    # cursor object for db acts as middle man between programmer and db
    cursor = get_db().cursor()

    # sql script to get nearest date data point
    sql = f'''SELECT * 
                FROM (
                    SELECT  ABS(JULIANDAY(Date(Date)) - JULIANDAY("{selected_date}")) as nearestDate,
                            FacilitiesData.FacilityID,
                            FacilityName,
                            Staffcases,
                            ResidentCases,
                            CountyName,
                            Date
                    FROM FacilitiesData, Facilities
                    ON Facilities.FacilityID = FacilitiesData.FacilityID
                    WHERE StateName="{state_name}"
                    ORDER BY nearestDate
                )
            GROUP BY FacilityID'''

    # fetch returns tuple
    facilities_table = cursor.execute(sql).fetchall()

    # creating dictionary
    data_dict = dict()

    # Order output of table
    for _, facility_id, facility_name, staff_cases, resident_cases, county_name, date in facilities_table:
        data_dict[facility_id] = {
            "facility_name": facility_name,
            "staff_cases": staff_cases,
            "resident_cases": resident_cases,
            "county_name": county_name,
            "date": date
        }

    return data_dict


# returns the max and min date for counties for given state for data selector restriction
def max_min_date_county(state_name='California'):
    cursor = get_db().cursor()
    sql = f'SELECT MAX (Date) FROM CountiesData WHERE StateName="{state_name}"'
    max_date = datetime.fromisoformat(
        cursor.execute(sql).fetchone()[0]).strftime("%Y-%m-%d")
    sql = f'SELECT MIN (Date) FROM CountiesData WHERE StateName="{state_name}"'
    min_date = datetime.fromisoformat(
        cursor.execute(sql).fetchone()[0]).strftime("%Y-%m-%d")

    return max_date, min_date

# closing db connection after program is closed
# flask function to close application layer
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# flask function for home
@app.route('/')
def home():

    # Get only california facility data from sql database
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Facilities WHERE StateName="California"'
    facilities = cursor.execute(sql)
    facilities_data = dict()

    for facility_id, facility_name, _, county_name, longitude, latitude in facilities:
        facilities_data[facility_id] = {
            "facility_name": facility_name,
            "county_name": county_name,
            "longitude": longitude,
            "latitude": latitude
        }

    # Get max and min date of county
    max_county_date, min_county_date = max_min_date_county(
        state_name='California')

    # returns website, facilities, max and min date to webpage.htl
    return render_template('webpage.html',
                           facilities=facilities_data,
                           max_county_date=max_county_date,
                           min_county_date=min_county_date)

# flask function whn user selecs a date
@app.route('/data/<selected_date>', methods=['GET', 'POST'])
def data_send(selected_date):

    county_data = get_counties_data(selected_date)
    facility_data = get_facilities_data(selected_date)
    return json.dumps({"counties": county_data, "facilities": facility_data})


if __name__ == "__main__":
    app.run()
