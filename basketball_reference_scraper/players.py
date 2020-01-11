import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from utils import get_player_suffix
except:
    from basketball_reference_scraper.utils import get_player_suffix

async def get_player_selector(suffix, selector):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/{suffix}')
    await page.waitForSelector(f'{selector}')
    table = await page.querySelectorEval(f'{selector}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]

def get_stats(name, stat_type='PER_GAME', playoffs=False, career=False):
    suffix = get_player_suffix(name).replace('/', '%2F')
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                  'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
        career_index = df[df['SEASON']=='Career'].index[0]
        if career:
            df = df.iloc[career_index+2:, :]
        else:
            df = df.iloc[:career_index, :]

        df = df.reset_index().dropna(axis=1).drop('index', axis=1)
        return df
