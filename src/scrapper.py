import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_current_matches(current_url):
    soup = get_url(current_url)
    match_anchors = soup.findAll("a",{"title":"H2H stats - match details"})
    match_urls = [i["href"] for i in match_anchors]
    # for each url get a dataframe row
    return match_urls
   

def get_finished_matches(finished_url):
    soup = get_url(finished_url)
    match_anchors = soup.findAll("a",{"title":"H2H stats - match details"})
    match_urls = [i["href"] for i in match_anchors]

    data = pd.DataFrame(columns=get_col_names())
    # for each url get a df
    for match in match_urls:
        temp = get_rows(match)
        # data = pd.concat([data,temp], ignore_index=True)
    return data

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
    # Next traverse through the 

def get_static_data(match_html):
    tr = match_html.find("tr", {"class": "tour_head unpair"})
    print(tr)

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
    finished_df = get_finished_matches(f'{fin_url}&dm={date}')
    finished_df.to_csv(f'./data/{get_file_name(date)}.csv', index = False, header = True, mode='w')

if __name__ == "__main__":
    main()