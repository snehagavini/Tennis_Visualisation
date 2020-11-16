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
    return match_urls

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

def main():
    date = '2020-10-31'
    url = 'http://www.tennislive.net/'
    curr_url, fin_url = get_menu_links(url)
    current_df = get_current_matches(curr_url)
    finished_df = get_finished_matches(f'{fin_url}&dm={date}')
    print(finished_df)

if __name__ == "__main__":
    main()