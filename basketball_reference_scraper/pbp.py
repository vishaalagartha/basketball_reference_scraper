import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from pyppeteer import launch
import asyncio

def get_suffix(date, team1, team2):
    r = get(f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'class': 'teams'}):
            for anchor in table.find_all('a'):
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    return suffix

async def get_pbp_helper(suffix):
    selector = f'#pbp'
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/boxscores/pbp{suffix}')
    await page.waitForSelector(f'{selector}')
    table = await page.querySelectorEval(f'{selector}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]

def format_df(df1):
    i0 = '1st Q'
    i1 = '1st Q.1'
    i2 = '1st Q.3'
    i3 = '1st Q.5'
    t1 = df1.iloc[0][i1]
    t2 = df1.iloc[0][i3]
    q = 'Q1'
    df = pd.DataFrame(columns=['Clock', t1, t2, f'{t1} Score', f'{t2} Score'])
    for index, row in df1.iterrows():
        d = {'Clock': float('nan'), t1: float('nan'), t2: float('nan'), f'{t1} Score': float('nan'), f'{t2} Score': float('nan')}
        if row[i0]=='2nd Q':
            q = 'Q2'
        elif row[i0]=='3rd Q':
            q = 'Q3'
        elif row[i0]=='4th Q':
            q = 'Q4'
        try:
            t = pd.to_datetime(row[i0])
            if t.hour==12:
                if q == 'Q1':
                    d['Clock'] = f'{q} {row[i0]}'
                    d[t1] = row[i1]
                    d[t2] = row[i1]
                    d[f'{t1} Score'] = 0
                    d[f'{t2} Score'] = 0
                    df = df.append(d, ignore_index=True)
                continue
        except:
            continue
        try:
            d['Clock'] = f'{q} {row[i0]}'
            d[t1] = row[i1]
            d[t2] = row[i3]
            scores = row[i2].split('-')
            d[f'{t1} Score'] = int(scores[0])
            d[f'{t2} Score'] = int(scores[1])
            df = df.append(d, ignore_index=True)
        except:
            pass
    return df

def get_pbp(date, team1, team2):
    date = pd.to_datetime(date)
    suffix = get_suffix(date, team1, team2).replace('/boxscores', '')
    df = asyncio.get_event_loop().run_until_complete(get_pbp_helper(suffix))
    df = format_df(df)
    return df
