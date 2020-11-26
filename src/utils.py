import pandas as pd

from datetime import datetime, timedelta
from collections import OrderedDict

def get_past_date(days = 0):
    format = '%Y-%m-%d'
    start = datetime.today() - timedelta(days = days)
    return datetime.strptime(start.strftime(format), format)
    
def get_matches_list(df, size = True):
    length = df.shape[0]
    if size and length > 5:
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

def get_matches(tournament, live, **kwargs):
    matches = pd.read_csv('./data/matches.csv')
    matches['index_date'] = pd.to_datetime(matches['index_date'], format = '%Y-%m-%d')
    tour = False
    results = dict()

    if live:
        curr_date = kwargs['curr_date']
        tournaments = matches[(matches['Tournament'] == tournament) & (matches['index_date'] == curr_date)]
        tour = True
    elif not live:
        start = kwargs['start']
        end = kwargs['end']
        tournaments = matches[(matches['Tournament'] == tournament) & (matches['index_date'] >= start) & (matches['index_date'] <= end)]
        tour = True

    if tour:
        results[tournament] = get_matches_list(tournaments[tournaments['Tournament'] == tournament], False)
    return results
    