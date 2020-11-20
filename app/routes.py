from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/live_tournaments")
def live_tournaments():
    tournaments = get_tournaments()
    return render_template("in.html", title = 'Live Tournaments')

@app.route("/finished_tournaments")
def finished_tournaments():
    tournaments = get_tournaments()
    return render_template("in.html", title = 'Finished Tournaments')

# Helper functions to get the data that has to be rendered in the pages
def get_tournaments():
    return list()