import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from utils import get_game_suffix
except:
    from basketball_reference_scraper.utils import get_game_suffix

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
        reserve_index = df1[df1['PLAYER']=='Reserves'].index[0]
        df1 = df1.drop(reserve_index).reset_index().drop('index', axis=1)
        soup = BeautifulSoup(r2.content, 'html.parser')
        table = soup.find('table')
        df2 = pd.read_html(str(table))[0]
        df2.columns = list(map(lambda x: x[1], list(df2.columns)))
        df2.rename(columns = {'Starters': 'PLAYER'}, inplace=True)
        reserve_index = df2[df2['PLAYER']=='Reserves'].index[0]
        df2 = df2.drop(reserve_index).reset_index().drop('index', axis=1)
        return {team1: df1, team2: df2}
