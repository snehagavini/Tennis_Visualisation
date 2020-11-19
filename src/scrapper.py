import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import csv 
import os

def get_current_matches(current_url):
    soup = get_url(current_url)
    match_anchors = soup.findAll("a",{"title":"H2H stats - match details"})
    match_urls = [i["href"] for i in match_anchors]
    # for each url get a dataframe row
    return match_urls
   

def get_finished_matches(finished_url, date):
    soup = get_url(finished_url)
    match_anchors = soup.findAll("a",{"title":"H2H stats - match details"})
    match_urls = [i["href"] for i in match_anchors]

    # for each url get a df
    for match in match_urls:
        finished_df = get_rows(match)
        if os.path.exists(f'./data/{get_file_name(date)}.csv'):       
            finished_df.to_csv(f'./data/{get_file_name(date)}.csv', index = False, header = False, mode='a')
        else:
            finished_df.to_csv(f'./data/{get_file_name(date)}.csv', index = False, header = True, mode='w')
        time.sleep(0.5)
        
    

def get_col_names():
    return ['player1_name',
            'player2_name',
            'set_index',
            'player1_game_score',
            'player2_game_score',
            'server',
            'points',
            'break_point',
            'tournament',
            'round',
            'date',
            'surface',
            'result'
            ]
        
def get_rows(match):
    match_html = get_url(match)
    fixed_data = get_static_data(match_html)
    scores_data = get_dynamic_data(match_html)
    rows = list()
    for k,v in scores_data.items():
        for score,points in v.items():
            rows.extend(merge_static_dynamic(k,score,points,fixed_data))
    
    return pd.DataFrame.from_records(rows,columns = get_col_names())

def merge_static_dynamic(set,score,points,fixed_data):
    result_list = list()
    row_list = {'player1': fixed_data['player1_name'],
                'player2': fixed_data['player2_name'],
                'set':set,
                'p1_score':score.split('-')[0],
                'p2_score':score.split('-')[1],
                'server':points[-1],
                'points': 0,
                'break_point': '',
                'tournament':fixed_data['tournament'],
                'round': fixed_data['round'],
                'date': fixed_data['date'],
                'surface': fixed_data['surface'],
                'result': fixed_data['result']
                }
    for i in range(len(points)-1):
        row_list['points'] = points[i]
        if 'BP' in points[i]:
            row_list['break_point'] = 'BP'
        result_list.append(list(row_list.values()))
    
    return result_list
        

def get_static_data(match_html):
    tr = match_html.find("tr", {"class": "tour_head unpair"})
    static_data = dict()    
    match_details = tr.findAll("td")
    static_cols = ['date','round','player1_name','player2_name', 'result','tournament','surface']
    for index in range(len(static_cols)):
        static_data[static_cols[index]] = match_details[index].text
    
    return static_data

def get_dynamic_data(match_html):
    scores_div = match_html.find("div", {"id": "ff_p"})
    set_tables = scores_div.findAll('table', {'class': 'table_stats_match'})
    dynamic_data = dict()
    for set in range(len(set_tables)):
        dynamic_data[set+1] = get_scores(set_tables[set])

    return dynamic_data


def get_scores(set_table):
    rows = set_table.findChildren('tr')[1:-1]
    score_dict = dict()
    for row_index in range(0,len(rows), 2):
        score , serve = get_current_score(rows[row_index])
        points = get_points(rows[row_index + 1])
        points.append(serve)
        score_dict[score] = points

    return score_dict

# Correct the function reflect the score and the serve
def get_current_score(row):
    server = row.text
    score = ''
    
    cells = row.findAll("td")
    score = cells[1].text
    server = server.replace(score,'')
    return score, server

# make the point to win in the last row i.e, if win=True
def get_points(row):
    return row.find("td").text.split(',')


def get_players_data(match_url):
    pass

def get_menu_links(url):
    soup = get_url(url)
    ul = soup.find("ul", {"id": "topmenu_full"})
    li_list = ul.findChildren("li" , recursive=False)
    url_list = []
    for i in [0,2]:
        url_list.append(li_list[i].findChildren("a")[0]["href"])
    return url_list[0], url_list[1]

def get_url(url):
    req = urlopen(url)
    html = str(req.read())
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_file_name(date):
    return date.replace('-','')

def main():
    date = '2020-10-31'
    url = 'http://www.tennislive.net/'
    curr_url, fin_url = get_menu_links(url)
    get_finished_matches(f'{fin_url}&dm={date}', date)

if __name__ == "__main__":
    main()