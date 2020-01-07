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

async def get_box_scores_helper(suffix, team1, team2, period='GAME', stat_type='BASIC'):
    period = period.lower()
    stat_type=stat_type.lower()
    selector1 = f'#box-{team1}-{period}-{stat_type}'
    selector2 = f'#box-{team2}-{period}-{stat_type}'
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com{suffix}')
    await page.waitForSelector(f'{selector1}')
    await page.waitForSelector(f'{selector2}')
    table1 = await page.querySelectorEval(f'{selector1}', '(element) => element.outerHTML')
    table2 = await page.querySelectorEval(f'{selector2}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table1)[0], pd.read_html(table2)[0]

def get_box_scores(date, team1, team2, period='GAME', stat_type='BASIC'):
    date = pd.to_datetime(date)
    suffix = get_suffix(date, team1, team2)
    df1, df2 = asyncio.get_event_loop().run_until_complete(get_box_scores_helper(suffix, team1, team2, period, stat_type))
    df1.columns = list(map(lambda x: x[1], df1.columns))
    df1.rename(columns={'Starters': 'Players'}, inplace=True)
    df1 = df1[df1['Players']!='Reserves']
    df2.columns = list(map(lambda x: x[1], df2.columns))
    df2.rename(columns={'Starters': 'Players'}, inplace=True)
    df2 = df2[df2['Players']!='Reserves']
    return {team1: df1, team2: df2}
