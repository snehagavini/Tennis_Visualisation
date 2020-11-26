from flask import render_template
from app import app
from datetime import datetime, timedelta
import pandas as pd
from collections import OrderedDict

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/live_tournaments")
def live_tournaments():
    format = '%Y-%m-%d'
    curr_date = get_past_date()
    tournaments = get_tournaments(live = True, curr_date = curr_date)
    return render_template("tournament.html", title = 'Live Tournaments', tournaments = tournaments)

@app.route("/finished_tournaments")
def finished_tournaments():
    format = '%y-%m-%d'
    default_start = get_past_date(4)
    default_end = get_past_date(1)
    tournaments = get_tournaments(live = False, start = default_start, end = default_end)
    return render_template("tournament.html", title = 'Finished Tournaments', tournaments = tournaments)

@app.route("/matches/<filename>")
def view_match_data(filename):
    print(filename)
    return render_template('match.html', filename = filename, title = 'Tennis Visualization')
#W25Las_221120_fin_KaiaKanepi_MayarSherif
@app.route("/test")
def test():
    return render_template('test.html')

# Helper functions to get the data that has to be rendered in the pages
def get_past_date(days = 0):
    format = '%Y-%m-%d'
    start = datetime.today() - timedelta(days = days)
    return datetime.strptime(start.strftime(format), format)
    
def get_matches_list(df):
    length = df.shape[0]
    if length > 5:
        df = df.iloc[:5]
    
    results = df.to_dict('records', into=OrderedDict)
    results.append(length)

    return results

def get_tournaments(live, **kwargs):
    matches = pd.read_csv('./data/matches.csv')
    matches['index_date'] = pd.to_datetime(matches['index_date'], format = '%Y-%m-%d')
    tour = False
    results = dict()

    if live:
        curr_date = kwargs['curr_date']
        tournaments = matches[matches['index_date'] == curr_date]
        tour = True
    elif not live:
        start = kwargs['start']
        end = kwargs['end']
        tournaments = matches[(matches['index_date'] >= start) & (matches['index_date'] <= end)]
        tour = True

    if tour:
        tourn_list = tournaments['Tournament'].value_counts().index.to_list()
        for tournament in tourn_list:
            results[tournament] = get_matches_list(tournaments[tournaments['Tournament'] == tournament])
    return results


with app.test_request_context():
    print(url_for('matches', filename = 'samba'))