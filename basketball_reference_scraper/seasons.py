import pandas as pd
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup

def get_schedule(season, playoffs=False):
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May']
    df = pd.DataFrame()
    for month in months:
        r = get(f'https://www.basketball-reference.com/leagues/NBA_{season}_games-{month.lower()}.html')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            month_df = pd.read_html(str(table))[0]
            df = df.append(month_df)
    df = df.reset_index()
    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']
    playoff_loc = df[df['DATE']=='Playoffs']
    if len(playoff_loc.index)>0:
        playoff_index = playoff_loc.index[0]
    else:
        playoff_index = len(df)
    if playoffs:
        df = df[playoff_index+1:]
    else:
        df = df[:playoff_index]
    df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
    return df

def get_standings(date=None):
    if date is None:
        date = datetime.now()
    else:
        date = pd.to_datetime(date)
    d = {}
    r = get(f'https://www.basketball-reference.com/friv/standings.fcgi?month={date.month}&day={date.day}&year={date.year}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        e_table = soup.find('table', attrs={'id': 'standings_e'})
        e_df = pd.read_html(str(e_table))[0]
        w_table = soup.find('table', attrs={'id': 'standings_w'})
        w_df = pd.read_html(str(w_table))[0]
        e_df.rename(columns={'Eastern Conference': 'TEAM'}, inplace=True)
        w_df.rename(columns={'Western Conference': 'TEAM'}, inplace=True)
        d['EASTERN_CONF'] = e_df
        d['WESTERN_CONF'] = w_df
    return d
