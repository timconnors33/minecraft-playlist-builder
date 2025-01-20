import requests
from bs4 import BeautifulSoup
import os
import json
import re

PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"
JOINED_THIS_SEASON_SPAN_ID = "Joined_This_Season"
RETURNED_FROM_PREV_SEASON_SPAN_ID = "Returned_From_Previous_Season"
SEASON_1_HERMITS_SPAN_ID = "Hermits"
HERMITS_HEADER_SPAN_ID = "Hermits"


class SeasonLink():
    def __init__(self, internal_link, text):
        self.internal_link = internal_link
        self.text = text


class SeasonAppearance():
    def __init__(self, youtube_internal_link, link_type):
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type

'''
def writeSeasonAppearancesToFile():
'''

def parseWikiPages():
    season_links = parseSeriesPage()
    for season_link in season_links:
        print(season_link.text)
        season_appearances = parseSeasonPage(season_page_internal_link=season_link.internal_link)
        for season_appearance in season_appearances:
            print(json.dumps(season_appearance.__dict__))

def parseSeasonTableBodies(table_bodies):
    youtube_link_pattern = re.compile(r'https://youtube.com/|https://www.youtube.com/|http://www.youtube.com/')
    season_appearances = []
    for table_body in table_bodies:
        anchors = table_body.find_all('a')
        for anchor in anchors:
            if anchor.has_attr('href') and youtube_link_pattern.match(anchor['href']):
                youtube_internal_link = anchor['href'] \
                    .replace('https://youtube.com/', '') \
                    .replace('https://www.youtube.com/', '') \
                    .replace('http://www.youtube.com/', '')
                link_type = 'channel'
                if 'list=PL' in youtube_internal_link:
                    link_type = 'playlist'
                season_appearance = SeasonAppearance(youtube_internal_link=youtube_internal_link, link_type=link_type)
                season_appearances.append(season_appearance)
    return season_appearances

def getHermitTableBodies(soup, season_link):
    table_bodies = []
    hermits_header_span = soup.find(id=HERMITS_HEADER_SPAN_ID)
    if season_link == "Season_1":
        table_bodies.append(hermits_header_span.find_next('tbody'))
    else:
        span_text_pattern = re.compile(r'Returning|Returned|Joined This Season|From Previous')
        matching_spans = hermits_header_span.find_all_next(string=span_text_pattern)
        for matching_span in matching_spans:
            table_bodies.append(matching_span.find_next('tbody'))
    return table_bodies

def parseSeasonPage(season_page_internal_link):
    filepath = './data/' + season_page_internal_link + '.json'
    if not os.path.exists(filepath):
        r = requests.get(f"https://hermitcraft.fandom.com/api.php?action=parse&page={season_page_internal_link}&format=json")
        htmlData = r.json()['parse']['text']['*']
        with open(filepath, 'w') as f:
            json.dump(htmlData, f)

    with open(filepath, 'r') as f:
        htmlData = json.load(f)
    soup = BeautifulSoup(htmlData, 'html.parser')
    table_bodies = getHermitTableBodies(soup=soup, season_link=season_page_internal_link)
    season_appearances = parseSeasonTableBodies(table_bodies=table_bodies)
    return season_appearances


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