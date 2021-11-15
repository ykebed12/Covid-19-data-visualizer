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


app = Flask(__name__)

DATABASE = './facility_cases.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def get_counties_data(selected_date, state_name="California"):
    cursor = get_db().cursor()
    sql = f'SELECT * FROM CountiesData WHERE StateName="{state_name}" and Date="{selected_date}"'

    # sql = f'''SELECT * FROM tb
    #                 (SELECT * FROM CountiesData
    #                     WHERE StateName="{state_name};"
    #                     ORDER BY ABS( JULIANDAY(Date)  - JULIANDAY("{selected_date}") )
    #                 ) as tb
    #             GROUP BY CountyName
    #             '''

    countiesTable = cursor.execute(sql).fetchall()
    print(countiesTable)
    data_dict = dict()

    # Order in sql CountiesData table
    # `DataID` , `CountyName`,  `StateName`, `Cases` , `Deaths`,  `Date`,
    for _, county_name, _, cases, deaths, date in countiesTable:
        data_dict[county_name] = {"Cases": cases,
                                  "Deaths": deaths,
                                  "Closest_Date": date}

    return data_dict


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():

    # Get only california facility data from sql database
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Facility WHERE StateName="California"'
    facilities = list(cursor.execute(sql))

    # Get max and min date of county
    max_county_date, min_county_date = max_min_date_county(
        state_name='California')

    return render_template('webpage.html',
                           dir_of_counties=dir_of_counties,
                           facilities=facilities,
                           max_county_date=max_county_date,
                           min_county_date=min_county_date,
                           max_state_cases=max_state_cases(state_name='California'))


@app.route('/county_data/<selected_date>', methods=['GET', 'POST'])
def county_data_send(selected_date):

    county_data = get_counties_data(selected_date)
    return json.dumps(county_data)


if __name__ == "__main__":
    app.run()
