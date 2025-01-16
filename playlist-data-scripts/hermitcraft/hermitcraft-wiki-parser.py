import requests
from bs4 import BeautifulSoup
import os
import json

"""
Only get the HTML data if the data file does not currently exist to limit requests
sent to the wiki server. TODO : determine a protocol for re-fetching information
from the wiki in order to stay up-to-date.
"""
if not os.path.exists('wiki-page.json'):
    r = requests.get("https://hermitcraft.fandom.com/api.php?action=parse&page=Series&format=json")
    htmlData = r.json()['parse']['text']
    with open('wiki-page.json', 'w') as f:
        json.dump(htmlData, f)

with open('wiki-page.json', 'r') as f:
    htmlData = json.load(f)
    soup = BeautifulSoup(htmlData, 'html.parser')
    print(soup.prettify)