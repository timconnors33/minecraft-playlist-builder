import requests
from bs4 import BeautifulSoup
import os
import json
import re


PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"
HERMITS_HEADER_SPAN_ID = "Hermits"


class SeasonLink():
    def __init__(self, internal_link, text, is_current_season):
        self.internal_link = internal_link
        self.text = text
        self.is_current_season = is_current_season


class SeasonAppearanceLink():
    def __init__(self, youtube_internal_link, link_type):
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type


def writeSeasonAppearancesToFile():
    # TODO: This should be extracted to a more general-purpose, reusable function at
    # some point
    all_series_list = []
    series_data = parseWikiPages()
    all_series_list.append(series_data)
    filepath = './data/hermitcraft/season-appearances.json'
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump(all_series_list, f)


def getSoup(filepath, uri):
    if not os.path.exists(filepath):
        r = requests.get(uri)
        htmlData = r.json()['parse']['text']['*']
        with open(filepath, 'w') as f:
            json.dump(htmlData, f)
    else:
        with open(filepath, 'r') as f:
            htmlData = json.load(f)
    soup = BeautifulSoup(htmlData, 'html.parser')

    return soup


def parseWikiPages():
    series = {}
    seasons = []
    season_appearances = []
    season_links = parseSeriesPage()
    for season_link in season_links:
        cur_season = {}
        cur_season_appearances = []
        cur_season_appearance_links = parseSeasonPage(season_page_internal_link=season_link.internal_link)
        for cur_season_appearance_link in cur_season_appearance_links:
            cur_season_appearances.append(cur_season_appearance_link.__dict__)
        cur_season['title'] = season_link.text
        cur_season['is_current_season'] = season_link.is_current_season
        cur_season['season_appearances'] = cur_season_appearances
        seasons.append(cur_season)
    series['title'] = 'Hermitcraft'
    series['seasons'] = seasons
    print(json.dumps(series, indent=4))
    return series


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
                season_appearance = SeasonAppearanceLink(youtube_internal_link=youtube_internal_link, link_type=link_type)
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
    filepath = './data/hermitcraft/wiki-pages/' + season_page_internal_link + '.json'
    soup = getSoup(filepath=filepath, uri=f"https://hermitcraft.fandom.com/api.php?action=parse&page={season_page_internal_link}&format=json")

    table_bodies = getHermitTableBodies(soup=soup, season_link=season_page_internal_link)
    season_appearances = parseSeasonTableBodies(table_bodies=table_bodies)

    return season_appearances


def parseSeriesTable(soup, series_table_id):
    list_of_links = []
    table_body = soup.find(id=series_table_id).find_next("tbody")
    anchors = table_body.find_all('a')
    for anchor in anchors:
        if anchor.has_attr('href') and anchor['href'].startswith('/wiki/'):
            is_current_season = False
            if series_table_id == CUR_VANILLA_SEASONS_SPAN_ID:
                is_current_season = True
            season_link = SeasonLink(internal_link=anchor['href'].replace('/wiki/', ''), text=anchor.get_text(), is_current_season=is_current_season)
            list_of_links.append(season_link)

    return list_of_links


def parseSeriesPage():
    """
    Only get the HTML data if the data file does not currently exist to limit requests
    sent to the wiki server. TODO : determine a protocol for re-fetching information
    from the wiki in order to stay up-to-date. Or just remove this functionality in production and run
    the script at a regular time interval. This is mostly only included for development purposes.
    """

    soup = getSoup(filepath='./data/hermitcraft/wiki-pages/series-wiki-page.json', uri="https://hermitcraft.fandom.com/api.php?action=parse&page=Series&format=json")
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
                if cur_season_link.is_current_season:
                    season_link.is_current_season = True
        if not isDuplicate:
            season_links.append(cur_season_link)

    return season_links


writeSeasonAppearancesToFile()