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
    df = df.drop(['Unnamed: 5', 'index'], axis=1)
    if len(df.columns)==6:
        df.columns = ['Date', 'Visitor', 'Visitor Pts', 'Home', 'Home Pts', 'Attendance']
    elif len(df.columns)==5:
        df.columns = ['Date', 'Visitor', 'Visitor Pts', 'Home', 'Home Pts']
    playoff_index = df[df['Date']=='Playoffs'].index[0]
    if playoffs:
        df = df[playoff_index+1:]
    else:
        df = df[:playoff_index]
    df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x))
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
        d['Eastern Conference'] = e_df
        d['Western Conference'] = w_df
    return d
