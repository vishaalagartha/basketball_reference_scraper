import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

try:
    from utils import get_game_suffix
except:
    from basketball_reference_scraper.utils import get_game_suffix

def get_pbp_helper(suffix):
    selector = f'#pbp'
    r = get(f'https://www.basketball-reference.com/boxscores/pbp{suffix}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table', attrs={'id': 'pbp'})
        return pd.read_html(str(table))[0]

def format_df(df1):
    df1.columns = list(map(lambda x: x[1], list(df1.columns)))
    t1 = list(df1.columns)[1].upper()
    t2 = list(df1.columns)[5].upper()
    q = 1
    df = None
    for index, row in df1.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row['Time']=='2nd Q':
            q = 2
        elif row['Time']=='3rd Q':
            q = 3
        elif row['Time']=='4th Q':
            q = 4
        elif 'OT' in row['Time']:
            q = row['Time'][0]+'OT'
        try:
            d['QUARTER'] = q
            d['TIME_REMAINING'] = row['Time']
            scores = row['Score'].split('-')
            d[f'{t1}_SCORE'] = int(scores[0])
            d[f'{t2}_SCORE'] = int(scores[1])
            d[f'{t1}_ACTION'] = row[list(df1.columns)[1]]
            d[f'{t2}_ACTION'] = row[list(df1.columns)[5]]
            if df is None:
                df = pd.DataFrame(columns = list(d.keys()))
            df = df.append(d, ignore_index=True)
        except:
            continue
    return df

def get_pbp(date, team1, team2):
    date = pd.to_datetime(date)
    suffix = get_game_suffix(date, team1, team2).replace('/boxscores', '')
    df = get_pbp_helper(suffix)
    df = format_df(df)
    return df
