from flask import render_template, url_for
from app import app
from src import utils

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/live_tournaments")
def live_tournaments():
    curr_date = utils.get_past_date()
    tournaments = utils.get_tournaments(live = True, curr_date = curr_date)
    return render_template("tournament.html", title = 'Live Tournaments', tournaments = tournaments, matches_url = 'live_matches')

@app.route("/finished_tournaments")
def finished_tournaments():
    default_start = utils.get_past_date(4)
    default_end = utils.get_past_date(1)
    tournaments = utils.get_tournaments(live = False, start = default_start, end = default_end)
    return render_template("tournament.html", title = 'Finished Tournaments', tournaments = tournaments, matches_url = 'finished_matches')

@app.route("/matches/<filename>", methods = ['GET'])
def matches(filename):
    return render_template('match.html', filename = filename, title = 'Tennis Visualization')

@app.route("/live_matches/<tournament>")
def live_matches(tournament):
    curr_date = utils.get_past_date()
    matches_list = utils.get_matches(tournament, live = True, curr_date = curr_date)
    return render_template("matches_list.html", matches = matches_list, title = tournament)

@app.route("/finished_matches/<tournament>")
def finished_matches(tournament):
    default_start = utils.get_past_date(4)
    default_end = utils.get_past_date(1)
    matches_list = utils.get_matches(tournament, live = False, start = default_start, end = default_end)
    return render_template("matches_list.html", matches = matches_list, title = tournament)
