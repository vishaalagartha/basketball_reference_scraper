import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR

def get_roster(team, season_end_year):
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F{team}%2F{season_end_year}.html&div=div_roster')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                        'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
        df['BIRTH_DATE'] = df['BIRTH_DATE'].apply(lambda x: pd.to_datetime(x))
        df['NATIONALITY'] = df['NATIONALITY'].apply(lambda x: x.upper())
    return df

def get_team_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format=='TOTAL':
        selector = 'div_team-stats-base'
    elif data_format=='PER_GAME':
        selector = 'div_team-stats-per_game'
    elif data_format=='PER_POSS':
        selector = 'div_team-stats-per_poss'
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM']==team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])

def get_opp_stats(team, season_end_year, data_format='PER_GAME'):
    if data_format=='TOTAL':
        selector = 'div_opponent-stats-base'
    elif data_format=='PER_GAME':
        selector = 'div_opponent-stats-per_game'
    elif data_format=='PER_POSS':
        selector = 'div_opponent-stats-per_poss'
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.columns = list(map(lambda x: 'OPP_'+x, list(df.columns)))
        df.rename(columns={'OPP_TEAM': 'TEAM'}, inplace=True)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM']==team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])

def get_team_misc(team, season_end_year):
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div=div_misc_stats')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = list(map(lambda x: x[1], list(df.columns)))
        league_avg_index = df[df['Team']=='League Average'].index[0]
        df = df[:league_avg_index]
        df['Team'] = df['Team'].apply(lambda x: x.replace('*', '').upper())
        df['TEAM'] = df['Team'].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(['Rk', 'Team'], axis=1)
        df.rename(columns = {'Age': 'AGE', 'Pace': 'PACE', 'Arena': 'ARENA', 'Attend.': 'ATTENDANCE', 'Attend./G': 'ATTENDANCE/G'}, inplace=True)
        df.loc[:, 'SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
        s = df[df['TEAM']==team]
        return pd.Series(index=list(s.columns), data=s.values.tolist()[0])

def get_roster_stats(team, season_end_year, data_format='PER_GAME', playoffs=False):
    if playoffs:
        period = 'playoffs'
    else:
        period = 'leagues'
    selector = data_format.lower()
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2F{period}%2FNBA_{season_end_year}_{selector}.html&div=div_{selector}_stats')
    df = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df2 = pd.read_html(str(table))[0]
        for index, row in df2.iterrows():
            if row['Tm']==team:
                if df is None:
                    df = pd.DataFrame(columns=list(row.index)+['SEASON'])
                row['SEASON'] = f'{season_end_year-1}-{str(season_end_year)[2:]}'
                df = df.append(row)
        df.rename(columns = {'Player': 'PLAYER', 'Age': 'AGE', 'Tm': 'TEAM', 'Pos': 'POS'}, inplace=True)
        df = df.reset_index().drop(['Rk', 'index'], axis=1)
        return df
