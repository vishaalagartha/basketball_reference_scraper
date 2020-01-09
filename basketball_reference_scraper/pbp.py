import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from pyppeteer import launch
import asyncio

try:
    from utils import get_game_suffix
except:
    from basketball_reference_scraper.utils import get_game_suffix

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
    t1 = df1.iloc[0][i1].upper()
    t2 = df1.iloc[0][i3].upper()
    q = 1
    df = pd.DataFrame(columns=['QUARTER', 'TIME_REMAINING', f'{t1}_ACTION', f'{t2}_ACTION', f'{t1}_SCORE', f'{t2}_SCORE'])
    for index, row in df1.iterrows():
        d = {'QUARTER': float('nan'), 'TIME_REMAINING': float('nan'), f'{t1}_ACTION': float('nan'), f'{t2}_ACTION': float('nan'), f'{t1}_SCORE': float('nan'), f'{t2}_SCORE': float('nan')}
        if row[i0]=='2nd Q':
            q = 2
        elif row[i0]=='3rd Q':
            q = 3
        elif row[i0]=='4th Q':
            q = 4
        try:
            t = pd.to_datetime(row[i0])
            if t.hour==12:
                if q == 'Q1':
                    d['QUARTER'] = q
                    d['TIME_REMAINING'] = row[i0]
                    d[f'{t1}_ACTION'] = row[i1]
                    d[f'{t2}_ACTION'] = row[i1]
                    d[f'{t1}_SCORE'] = 0
                    d[f'{t2}_SCORE'] = 0
                    df = df.append(d, ignore_index=True)
                continue
        except:
            continue
        try:
            d['QUARTER'] = q
            d['TIME_REMAINING'] = row[i0]
            d[f'{t1}_ACTION'] = row[i1]
            d[f'{t2}_ACTION'] = row[i3]
            scores = row[i2].split('-')
            d[f'{t1}_SCORE'] = int(scores[0])
            d[f'{t2}_SCORE'] = int(scores[1])
            df = df.append(d, ignore_index=True)
        except:
            pass
    return df

def get_pbp(date, team1, team2):
    date = pd.to_datetime(date)
    suffix = get_game_suffix(date, team1, team2).replace('/boxscores', '')
    df = asyncio.get_event_loop().run_until_complete(get_pbp_helper(suffix))
    df = format_df(df)
    return df
