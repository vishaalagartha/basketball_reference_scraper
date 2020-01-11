import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import re

try:
    from utils import get_game_suffix
except:
    from basketball_reference_scraper.utils import get_game_suffix

def get_location(s):
    l = s.split(';')
    top = float(l[0][l[0].index(':')+1:l[0].index('px')])
    left = float(l[1][l[1].index(':')+1:l[1].index('px')])
    x = left/500.0*50
    y = top/472.0*(94/2)
    return {'x': str(x)[:4] + ' ft', 'y': str(y)[:4] + ' ft'}

def get_description(s):
    match = re.match(r'(\d)[a-z]{2} quarter, (\S*) remaining<br>(.*) \b(missed|made) (\d)-pointer from (\d*) ft', s)
    d = {}
    if match:
        groups = match.groups()
        d['QUARTER'] = int(groups[0])
        d['TIME_REMAINING'] = groups[1]
        d['PLAYER'] = groups[2]
        d['MAKE_MISS'] = 'MAKE' if groups[3]=='made' else 'MISS'
        d['VALUE'] = int(groups[4])
        d['DISTANCE'] = groups[5] + ' ft'
    return d


def get_shot_chart(date, team1, team2):
    date = pd.to_datetime(date)
    suffix = get_game_suffix(date, team1, team2).replace('/boxscores', '')
    r = get(f'https://www.basketball-reference.com/boxscores/shot-chart{suffix}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        shot_chart1_div = soup.find('div', attrs={'id': f'shots-{team1}'})
        shot_chart2_div = soup.find('div', attrs={'id': f'shots-{team2}'})
        df1 = pd.DataFrame()
        for div in shot_chart1_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df1 = df1.append(shot_df)
        df1 = df1.reset_index()
        df1 = df1.drop('index', axis=1)
        df2 = pd.DataFrame()
        for div in shot_chart2_div.find_all('div'):
            if 'style' not in div.attrs or 'tip' not in div.attrs:
                continue
            location = get_location(div.attrs['style'])
            description = get_description(div.attrs['tip'])
            shot_d = {**location, **description}
            shot_df = pd.DataFrame.from_dict([shot_d])
            df2 = df2.append(shot_df)
        df2 = df2.reset_index()
        df2 = df2.drop('index', axis=1)

        return {f'{team1}': df1, f'{team2}': df2}
