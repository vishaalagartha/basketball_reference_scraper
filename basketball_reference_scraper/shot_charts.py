import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from pyppeteer import launch
import asyncio
import re

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
        d['quarter'] = int(groups[0])
        d['time_remaining'] = groups[1]
        d['player'] = groups[2]
        d['type'] = 'MAKE' if groups[3]=='made' else 'MISS'
        d['value'] = int(groups[4])
        d['distance'] = groups[5] + ' ft'
    return d

async def get_shot_chart_helper(suffix, team1, team2):
    selector1 = '#shots-'+team1
    selector2 = '#shots-'+team2
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/boxscores/shot-chart{suffix}')
    await page.waitForSelector(f'{selector1}')
    await page.waitForSelector(f'{selector2}')
    div1 = await page.querySelectorEval(f'{selector1}', '(element) => element.outerHTML')
    div2 = await page.querySelectorEval(f'{selector2}', '(element) => element.outerHTML')
    await browser.close()
    return div1, div2

def get_shot_chart(date, team1, team2):
    date = pd.to_datetime(date)
    suffix = get_suffix(date, team1, team2).replace('/boxscores', '')
    shot_chart1, shot_chart2 = asyncio.get_event_loop().run_until_complete(get_shot_chart_helper(suffix, team1, team2))
    shot_chart1_div = BeautifulSoup(shot_chart1, 'html.parser')
    shot_chart2_div = BeautifulSoup(shot_chart2, 'html.parser')
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
