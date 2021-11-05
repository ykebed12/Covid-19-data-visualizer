# import webbrowser
# import http.server
# import socketserver
from flask import Flask, redirect, url_for, render_template
from flask import current_app, g
from flask.cli import with_appcontext
from os import listdir
from os.path import isfile, join, isdir
import sqlite3


app = Flask(__name__)

DATABASE = './facility_cases.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def home():

    # Get geojson directories of california counties
    counties_dir = './static/USA/CA/'
    dir_of_counties = [f"/USA/CA/{filename}" for filename in listdir(
        counties_dir) if isfile(join(counties_dir, filename))]

    # counties_dir = './static/USA/'
    # dir_of_counties = []

    # for folder in listdir(counties_dir):

    #     folder_dir = join(counties_dir, folder)

    #     if isdir(folder_dir):
    #         for county_filename in listdir(folder_dir):
    #             county_dir = join(folder_dir, county_filename)
    #             if isfile(county_dir):
    #                 dir_of_counties.append(county_dir)

    # Get geojson directories of states
    # states_dir = './static/USA/'
    # dir_of_states = [f"/USA/{filename}" for filename in listdir(
    #     states_dir) if isfile(join(states_dir, filename))]

    # Get only california facility data from sql database
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Facility WHERE StateName="California"'
    facilities = list(cursor.execute(sql))

    return render_template('webpage.html', dir_of_counties=dir_of_counties, facilities=facilities,)


if __name__ == "__main__":
    app.run()
