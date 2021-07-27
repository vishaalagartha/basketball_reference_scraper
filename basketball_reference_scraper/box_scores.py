import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import re

try:
    from utils import get_game_suffix, remove_accents
    from players import get_stats 
except:
    from basketball_reference_scraper.utils import get_game_suffix, remove_accents
    from basketball_reference_scraper.players import get_stats

def get_box_scores(date, team1, team2, period='GAME', stat_type='BASIC'):
    date = pd.to_datetime(date)
    suffix = get_game_suffix(date, team1, team2).replace('/', '%2F')
    r1 = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_box-{team1}-{period.lower()}-{stat_type.lower()}')
    r2 = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_box-{team2}-{period.lower()}-{stat_type.lower()}')
    if r1.status_code==200 and r2.status_code==200:
        soup = BeautifulSoup(r1.content, 'html.parser')
        table = soup.find('table')
        df1 = pd.read_html(str(table))[0]
        df1.columns = list(map(lambda x: x[1], list(df1.columns)))
        df1.rename(columns = {'Starters': 'PLAYER'}, inplace=True)
        df1['PLAYER'] = df1['PLAYER'].apply(lambda name: remove_accents(name, team1, date.year))
        reserve_index = df1[df1['PLAYER']=='Reserves'].index[0]
        df1 = df1.drop(reserve_index).reset_index().drop('index', axis=1)
        soup = BeautifulSoup(r2.content, 'html.parser')
        table = soup.find('table')
        df2 = pd.read_html(str(table))[0]
        df2.columns = list(map(lambda x: x[1], list(df2.columns)))
        df2.rename(columns = {'Starters': 'PLAYER'}, inplace=True)
        df2['PLAYER'] = df2['PLAYER'].apply(lambda name: remove_accents(name, team2, date.year))
        reserve_index = df2[df2['PLAYER']=='Reserves'].index[0]
        df2 = df2.drop(reserve_index).reset_index().drop('index', axis=1)
        return {team1: df1, team2: df2}

def get_all_star_box_score(year: int):
    """ Returns box star for all star game in a given year

    Args:
        year (int): the year of the all star game 

    Raises:
        ValueError: if invalid year is intered 
        ConnectionError: when server cannot be reached

    Returns:
        dict: dictionary containing entries (team name, box score dataframe) for each team 
    """
    if year >= datetime.now().year or year < 1951:
        raise ValueError('Please enter a valid year')
    r = get(f'https://www.basketball-reference.com/allstar/NBA_{year}.html')
    if r.status_code == 200:
        dfs = []
        soup = BeautifulSoup(r.content, 'html.parser')
        team_names = list(map(lambda el: el.text, soup.select('div.section_heading > h2')[1:3]))
        for table in soup.find_all('table')[1:3]:
            df = pd.read_html(str(table))[0]
            df.columns = list(map(lambda x: x[1], list(df.columns)))
            df.rename(columns = {'Starters': 'PLAYER', 'Tm': 'TEAM'}, inplace=True)
            reserve_index = df[df['PLAYER']=='Reserves'].index[0]
            df = df.drop(reserve_index).reset_index().drop('index', axis=1) 
            #drop team totals row (always last), totals row
            totals_index = df[df['MP'] == 'Totals'].index[0]
            df = df.drop(totals_index).reset_index().drop('index', axis=1) 
            df = df.drop(df.tail(1).index).reset_index().drop('index', axis=1) 
            # sometimes there is a nan player
            dfs.append(df)
        res = {team_names[0]: dfs[0], team_names[1]: dfs[1]}
        # add DNPs for all-star roster purposes
        # the all-star team each dnp is on is in parens. for some reasons this captures parens
        dnp_allstar_teams = re.findall(r'\((.*?)\)', soup.select('ul.page_index > li > div')[0].text)
        for i, dnp in enumerate(map(lambda el: el.text, soup.select('ul.page_index > li > div > a'))):
            # check if the player is already in the dataframe because sometimes replacements are
            # listed twice (e.g. 1980)
            as_team = dnp_allstar_teams[i]
            if dnp not in res[as_team]['PLAYER'].values:
                new_row = {col: 0 for col in df.columns if col != 'PLAYER' and col != 'TEAM'}
                new_row['PLAYER'] = dnp
                # infer the added player's real team 
                stats_df = get_stats(dnp, ask_matches=False)
                team = stats_df.query(f'SEASON == {year-1}-{year}').head(1)['TEAM']
                new_row['TEAM'] = team
                # set players allstar team from regexp
                res[as_team] = res[as_team].append(new_row, ignore_index=True)
        return res 
    else:
        raise ConnectionError('Request to basketball reference failed')

