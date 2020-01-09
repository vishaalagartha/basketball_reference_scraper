import pandas as pd
from pyppeteer import launch
from requests import get
from bs4 import BeautifulSoup
import asyncio

async def get_team_selector(team, season, selector):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(f'https://www.basketball-reference.com/teams/{team}/{season}.html')
    await page.waitForSelector(f'{selector}')
    table = await page.querySelectorEval(f'{selector}', '(element) => element.outerHTML')
    await browser.close()
    return pd.read_html(table)[0]

def get_roster(team, season):
    roster_df = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, '#roster'))
    roster_df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                        'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
    roster_df['BIRTH_DATE'] = roster_df['BIRTH_DATE'].apply(lambda x: pd.to_datetime(x))
    roster_df['NATIONALITY'] = roster_df['NATIONALITY'].apply(lambda x: x.upper())
    return roster_df

def get_team_series(team, season, data_format='PER_GAME'):
    series = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, '#team_and_opponent'))
    series = series.drop(['Unnamed: 0'], axis=1)
    if data_format=='TOTAL':
        final_series = series.iloc[0]
    elif data_format=='PER_GAME':
        final_series = series.iloc[1]
    elif data_format=='RANK':
        final_series = series.iloc[2]
    elif data_format=='Y/Y':
        final_series = series.iloc[3]
    return final_series

def get_opp_series(team, season, data_format='PER_GAME'):
    s1 = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, '#team_and_opponent'))
    s1 = s1.drop(['Unnamed: 0'], axis=1)
    if data_format=='TOTAL':
        s2 = s1.iloc[4]
    elif data_format=='PER_GAME':
        s2 = s1.iloc[5]
    elif data_format=='RANK':
        s2 = s1.iloc[6]
    elif data_format=='Y/Y':
        s2 = s1.iloc[7]
    indices = list(map(lambda x: 'OPP_'+x, list(s2.index)))
    final_series = pd.Series(data=s2.values, index=indices)
    return final_series

def get_roster_stats(team, season, data_format='PER_GAME', playoffs=False):
    if data_format=='PER_GAME':
        selector = 'per_game'
    elif data_format=='TOTALS':
        selector = 'totals'
    elif data_format=='PER_36':
        selector = 'per_minute'
    elif data_format=='PER_100_POSS':
        selector = 'per_poss'
    elif data_format=='ADVANCED':
        selector = 'advanced'

    if playoffs:
        selector = 'playoffs_'+selector
        
    selector = '#'+selector
    roster_df = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, selector))
    roster_df = roster_df.drop('Rk', axis=1)
    roster_df.rename(columns={'Unnamed: 1':'Name'}, inplace=True)
    roster_df = roster_df.dropna(axis=1)
    return roster_df

def get_team_misc(team, season, data_format='PER_GAME'):
    team_misc_df = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, '#team_misc'))
    index = list(map(lambda x: x[1], team_misc_df.columns))
    if data_format=='RANK':
        series = team_misc_df.iloc[1]
    else:
        series = team_misc_df.iloc[0]
    final_series = pd.Series(series.values, index = index)[1:]
    return final_series

def get_player_salaries(team, season):
    salaries_df = asyncio.get_event_loop().run_until_complete(get_team_selector(team, season, '#salaries2'))
    salaries_df.rename(columns={'Unnamed: 1':'Name'}, inplace=True)
    salaries_df = salaries_df.drop('Rk', axis=1)
    salaries_df.columns = ['NAME', 'SALARY']
    return salaries_df
