import requests
from bs4 import BeautifulSoup
import os
import json

PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"

"""
Only get the HTML data if the data file does not currently exist to limit requests
sent to the wiki server. TODO : determine a protocol for re-fetching information
from the wiki in order to stay up-to-date. Or just remove this functionality in production and run
the script at a regular time interval. This is mostly only included for development purposes.
"""
filepath = './data/series-wiki-page.json'
if not os.path.exists(filepath):
    r = requests.get("https://hermitcraft.fandom.com/api.php?action=parse&page=Series&format=json")
    htmlData = r.json()['parse']['text']['*']
    with open(filepath, 'w') as f:
        json.dump(htmlData, f)

with open(filepath, 'r') as f:
    htmlData = json.load(f)

soup = BeautifulSoup(htmlData, 'html.parser')

past_vanilla_seasons_table = soup.find(id=PAST_VANILLA_SEASONS_SPAN_ID).find_next("tbody")
anchors = past_vanilla_seasons_table.find_all('a')

for anchor in anchors:
    if anchor.has_attr('href') and anchor.has_attr('title'):
        link = anchor['href']
        name = anchor.get_text()
        print(link)
        print(name)