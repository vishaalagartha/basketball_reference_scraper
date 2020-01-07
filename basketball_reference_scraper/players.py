import pandas as pd
from pyppeteer import launch
from requests import get
from bs4 import BeautifulSoup
import asyncio

def get_player_suffix(name):
    last_name = name.split(' ')[-1]
    initial = last_name[0].lower()
    r = get(f'https://www.basketball-reference.com/players/{initial}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'id': 'players'}):
            for anchor in table.find_all('a'):
                if anchor.text==name:
                    return anchor.attrs['href']

async def get_player_selector(suffix, selector):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/{suffix}')
    await page.waitForSelector(f'{selector}')
    table = await page.querySelectorEval(f'{selector}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]

def get_stats(name, stat_type='PER_GAME', playoffs=False, career=False):
    suffix = get_player_suffix(name)
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    df= asyncio.get_event_loop().run_until_complete(get_player_selector(suffix, '#'+selector))
    career_index = df[df['Season']=='Career'].index[0]
    if career:
        df = df.iloc[career_index+2:, :]
    else:
        df = df.iloc[:career_index, :]

    df = df.dropna(axis=1)
    return df
