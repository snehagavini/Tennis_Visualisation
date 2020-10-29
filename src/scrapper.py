from urllib.request import urlopen
from bs4 import BeautifulSoup 

# add the fucntion later to read the url input from CLI/GUI
url = 'http://www.tennislive.net/'
# get the html of the url
req = urlopen(url)
#save to a html file
html = str(req.read())
with open("./data/index.html","w") as f:
    f.write(html)

soup = BeautifulSoup(html, 'html.parser')

for link in soup.find_all('a'):
    if link.get('href') == "http://www.tennislive.net/tennis_livescore.php?t=live":
        current_url = link.get('href')
    elif link.get('href') =="http://www.tennislive.net/tennis_livescore.php?t=fin":
        finished_url = link.get('href')

def get_current_matches(current_url):
    pass

def get_finished_matches(finished_url)
    pass

def get_players_data(match_url):
    pass