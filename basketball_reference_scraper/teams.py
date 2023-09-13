import pandas as pd
from requests import get
from bs4 import BeautifulSoup, Comment

try:
    from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from utils import remove_accents
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from basketball_reference_scraper.utils import remove_accents


def get_roster(team, season_end_year):
    r = get(
        f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                      'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
        # remove rows with no player name (this was the issue above)
        df = df[df['PLAYER'].notna()]
        df['PLAYER'] = df['PLAYER'].apply(
            lambda name: remove_accents(name, team, season_end_year))
        # handle rows with empty fields but with a player name.
        df['BIRTH_DATE'] = df['BIRTH_DATE'].apply(
            lambda x: pd.to_datetime(x) if pd.notna(x) else pd.NaT)
        df['NATIONALITY'] = df['NATIONALITY'].apply(
            lambda x: x.upper() if pd.notna(x) else '')

    return df


def get_team_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format == 'TOTAL':
        selector = 'div_totals-team'
    elif data_format == 'PER_GAME':
        selector = 'div_per_game-team'
    elif data_format == 'PER_POSS':
        selector = 'div_per_poss-team'
    r = get(
        f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team'] == 'League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM'] == team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])


def get_opp_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format == 'TOTAL':
        selector = 'div_totals-opponent'
    elif data_format == 'PER_GAME':
        selector = 'div_per_game-opponent'
    elif data_format == 'PER_POSS':
        selector = 'div_per_poss-opponent'
    r = get(
        f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team'] == 'League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.columns = list(map(lambda x: 'OPP_'+x, list(df.columns)))
        df.rename(columns={'OPP_TEAM': 'TEAM'}, inplace=True)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM'] == team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])


def get_team_misc(team, season_end_year):
    r = get(f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        tables = []
        for each in comments:
            if 'table' in str(each):
                try:
                    tables.append(pd.read_html(each, attrs = {'id': 'team_misc'}, header=1)[0])
                except:
                    continue
        df = pd.DataFrame(tables[0])
        df.columns = df.columns.str.replace(r'\.1','',regex=True)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        df['TEAM'] = team
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        return pd.Series(index=list(df.columns), data=df.values.tolist()[0])


def get_roster_stats(team: list, season_end_year: int, data_format='PER_GAME', playoffs=False):
    if playoffs:
        period = 'playoffs'
    else:
        period = 'leagues'
    selector = data_format.lower()
    r = get(
        f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2F{period}%2FNBA_{season_end_year}_{selector}.html&div=div_{selector}_stats')
    df = None
    possible_teams = [team]
    for s in TEAM_SETS:
        if team in s:
            possible_teams = s
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df2 = pd.read_html(str(table))[0]
        for index, row in df2.iterrows():
            if row['Tm'] in possible_teams:
                if df is None:
                    df = pd.DataFrame(columns=list(row.index)+['SEASON'])
                row['SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
                df = df.append(row)
        df.rename(columns={'Player': 'PLAYER', 'Age': 'AGE',
                  'Tm': 'TEAM', 'Pos': 'POS'}, inplace=True)
        df['PLAYER'] = df['PLAYER'].apply(
            lambda name: remove_accents(name, team, season_end_year))
        df = df.reset_index().drop(['Rk', 'index'], axis=1)
        return df

def get_team_ratings(*, team=[], season_end_year: int):

    # Scrape data from URL
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}_ratings.html&div=div_ratings')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]

        # Clean columns and indexes
        df = df.droplevel(level=0, axis=1)
        
        df.drop(columns=['Rk', 'Conf', 'Div', 'W', 'L', 'W/L%'], inplace=True)
        upper_cols = list(pd.Series(df.columns).apply(lambda x: x.upper()))
        df.columns = upper_cols

        df['TEAM'] = df['TEAM'].apply(lambda x: x.upper())
        df['TEAM'] = df['TEAM'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])

        # Add 'Season' column in and change order of columns
        df['SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        cols = df.columns.tolist()
        cols = cols[0:1] + cols[-1:] + cols[1:-1]
        df = df[cols]

        # Add the ability to either pass no teams (empty list), one team (str), or multiple teams (list)
        if len(team) > 0:
            if isinstance(team, str):
                list_team = []
                list_team.append(team)
                df = df[df['TEAM'].isin(list_team)]
            else:
                df = df[df['TEAM'].isin(team)]
                    
    return df
