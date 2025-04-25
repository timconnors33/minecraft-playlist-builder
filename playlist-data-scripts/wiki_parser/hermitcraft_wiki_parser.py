import requests
from bs4 import BeautifulSoup
import os
import json
import re
from urllib.parse import urlparse


PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"
HERMITS_HEADER_SPAN_ID = "Hermits"
SERIES_TITLE = "Hermitcraft"


class SeasonLink():
    def __init__(self, internal_link, text, is_current_season):
        self.internal_link = internal_link
        self.text = text
        self.is_current_season = is_current_season


class SeasonAppearanceLink():
    def __init__(self, youtube_internal_link, link_type):
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type

class SeasonAppearanceLinkAggregate():
    def __init__(self, series_title, season_title, is_current_season, youtube_internal_link, link_type):
        self.series_title = series_title
        self.season_title = season_title
        self.is_current_season = is_current_season
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type


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
    season_appearance_links = []
    season_links = parseSeriesPage()
    for season_link in season_links:
        cur_season_appearance_links = parseSeasonPage(season_page_internal_link=season_link.internal_link)
        for cur_season_appearance_link in cur_season_appearance_links:
            # TODO: This looks quite silly, but I want to filter out seasons 1-5 for now because not all
            # hermits from that era have playlists. However, (I think) all hermits from season 6 onward
            # who have channel links on the wiki pages do have valid playlists; sometimes they are
            # community-made.
            # https://stackoverflow.com/questions/5320525/regular-expression-to-match-last-number-in-a-string
            season_number = int(re.compile(r'.*(?:\D|^)(\d+)').findall(season_link.text)[0])
            if cur_season_appearance_link.link_type == 'playlist' or season_number >= 6:
                # TODO: Clean season text data if necessary
                cur_season_appearance_link_agg = SeasonAppearanceLinkAggregate(
                    series_title=SERIES_TITLE,
                    season_title=season_link.text,
                    is_current_season=season_link.is_current_season,
                    youtube_internal_link=cur_season_appearance_link.youtube_internal_link,
                    link_type=cur_season_appearance_link.link_type
                )
                season_appearance_links.append(cur_season_appearance_link_agg.__dict__)
    #print(json.dumps(season_appearance_links, indent=4))
    return season_appearance_links


def parseSeasonTableBodies(table_bodies):
    season_appearances = []
    for table_body in table_bodies:
        anchors = table_body.find_all('a')
        for anchor in anchors:
            # TODO: Assume that all anchors have an href or no?
            if anchor.has_attr('href'):
                parsed = urlparse(anchor['href'])
                if (parsed.scheme == 'http' or parsed.scheme == 'https') and (parsed.netloc == 'www.youtube.com' or parsed.netloc == 'youtube.com'):
                    if parsed.path == '/playlist' or 'list=PL' in parsed.query:
                        link_type = 'playlist'
                        youtube_internal_link = getPlaylistId(youtube_internal_link=parsed.query)
                    else:
                        link_type = 'channel'
                        youtube_internal_link = parsed.path
                        # Could maybe reformat this to not use any if statements and just get the string at parsed.path.count('/'),
                        # however I think this relationship is coincidential rather than intrinsic.
                        if parsed.path.count('/') == 1:
                            youtube_internal_link = parsed.path.split('/')[1]
                        if parsed.path.count('/') >= 2:
                            youtube_internal_link = parsed.path.split('/')[2]
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
    TODO: The time complexity on this is horrible, but the amount of elements involved should
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

def getPlaylistId(youtube_internal_link):
    # TODO: This looks silly, but I want to make sure not to extract another
    # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
    processed_link = 'PL' + (youtube_internal_link.split('list=PL', 1)[1]).split('&', 1)[0]
    return processed_link
