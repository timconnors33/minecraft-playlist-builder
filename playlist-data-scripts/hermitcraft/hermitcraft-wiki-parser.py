import requests
from bs4 import BeautifulSoup
import os
import json

PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"

class SeasonLink():
    def __init__(self, internal_link, text):
        self.internal_link = internal_link
        self.text = text

'''
def writeSeasonAppearancesToFile():
'''

def parseWikiPages():
    season_links = parseSeriesPage()
    for season_link in season_links:
        print(json.dumps(season_link.__dict__))
        parseSeasonPage(season_page_internal_link=season_link.internal_link)

def parseSeasonPage(season_page_internal_link):
    filepath = './data/' + season_page_internal_link + '.json'
    if not os.path.exists(filepath):
        r = requests.get(f"https://hermitcraft.fandom.com/api.php?action=parse&page={season_page_internal_link}&format=json")
        htmlData = r.json()['parse']['text']['*']
        with open(filepath, 'w') as f:
            json.dump(htmlData, f)

    with open(filepath, 'r') as f:
        htmlData = json.load(f)


def parseSeriesTable(soup, series_table_id):
    list_of_links = []
    table_body = soup.find(id=series_table_id).find_next("tbody")
    anchors = table_body.find_all('a')
    for anchor in anchors:
        if anchor.has_attr('href') and anchor['href'].startswith('/wiki/'):
            season_link = SeasonLink(internal_link=anchor['href'].replace('/wiki/', ''), text=anchor.get_text())
            list_of_links.append(season_link)
    return list_of_links

def parseSeriesPage():
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
    season_links = []
    past_season_links = parseSeriesTable(soup=soup, series_table_id=PAST_VANILLA_SEASONS_SPAN_ID)
    cur_season_links = parseSeriesTable(soup=soup, series_table_id=CUR_VANILLA_SEASONS_SPAN_ID)

    """
    The time complexity on this is horrible, but the amount of elements involved should
    be small enough to where it is not an issue.
    """
    season_links.extend(past_season_links)
    for cur_season_link in cur_season_links:
        isDuplicate = False
        for season_link in season_links:
            if season_link.internal_link == cur_season_link.internal_link and season_link.text == cur_season_link.text:
                isDuplicate = True
        if not isDuplicate:
            season_links.append(cur_season_link)

    return season_links

parseWikiPages()