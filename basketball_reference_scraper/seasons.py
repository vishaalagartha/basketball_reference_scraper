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
    df = df.dropna(axis='columns')
    df = df.reset_index()
    cols_to_remove = [x for x in df.columns if 'Unnamed' in x]
    cols_to_remove += [y for y in df.columns if 'Start' in y]
    cols_to_remove += [z for z in df.columns if 'Attend' in z]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['Date', 'Visitor', 'Visitor Pts', 'Home', 'Home Pts']
    playoff_index = df[df['Date']=='Playoffs'].index[0]
    if playoffs:
        df = df[playoff_index+1:]
    else:
        df = df[:playoff_index]
    df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x))
    df.rename(columns = {'Date': 'DATE', 'Visitor': 'VISITOR', 'Visitor Pts':
        'VISITOR_PTS', 'Home': 'HOME', 'Home Pts': 'HOME_PTS', 'Attendance':
        'ATTENDANCE'}, inplace=True)
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
