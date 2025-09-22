import re
import pandas as pd
from . import parser_utils

PAST_VANILLA_SEASONS_SPAN_ID = "Past_Vanilla_Seasons"
CUR_VANILLA_SEASONS_SPAN_ID = "Current_Vanilla_Seasons"
HERMITS_HEADER_SPAN_ID = "Hermits"
SERIES_TITLE = "Hermitcraft"

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
                cur_season_appearance_link_agg = parser_utils.SeasonAppearanceLinkAggregate(
                    series_title=SERIES_TITLE,
                    season_title=season_link.text,
                    is_current_season=season_link.is_current_season,
                    youtube_internal_link=cur_season_appearance_link.youtube_internal_link,
                    link_type=cur_season_appearance_link.link_type
                )
                season_appearance_links.append(cur_season_appearance_link_agg.__dict__)
    #print(json.dumps(season_appearance_links, indent=4))
    return pd.DataFrame(season_appearance_links)


def parseSeasonTableBodies(table_bodies):
    season_appearances = []
    for table_body in table_bodies:
        anchors = table_body.find_all('a')
        for anchor in anchors:
            # TODO: Assume that all anchors have an href or no?
            if anchor.has_attr('href'):
                season_appearance = parser_utils.parseYouTubeUri(uri=anchor['href'])
                if season_appearance:
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
    soup = parser_utils.getSoup(filepath=filepath, uri=f"https://hermitcraft.fandom.com/api.php?action=parse&page={season_page_internal_link}&format=json")

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
            season_link = parser_utils.SeasonLink(internal_link=anchor['href'].replace('/wiki/', ''), text=anchor.get_text(), is_current_season=is_current_season)
            list_of_links.append(season_link)

    return list_of_links


def parseSeriesPage():
    """
    Only get the HTML data if the data file does not currently exist to limit requests
    sent to the wiki server. TODO : determine a protocol for re-fetching information
    from the wiki in order to stay up-to-date. Or just remove this functionality in production and run
    the script at a regular time interval. This is mostly only included for development purposes.
    """

    soup = parser_utils.getSoup(filepath='./data/hermitcraft/wiki-pages/series-wiki-page.json', uri="https://hermitcraft.fandom.com/api.php?action=parse&page=Series&format=json")
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
