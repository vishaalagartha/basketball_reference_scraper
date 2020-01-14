import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR
except:
    from basketball_reference_scraper.constants import TEAM_TO_TEAM_ABBR

def get_injury_report():
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Ffriv%2Finjuries.fcgi&div=div_injuries')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.rename(columns = {'Player': 'PLAYER', 'Team': 'TEAM', 'Update': 'DATE', 'Description': 'DESCRIPTION'}, inplace=True)
        df['TEAM'] = df['TEAM'].apply(lambda x: TEAM_TO_TEAM_ABBR[x.upper()])
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
        df['STATUS'] = df['DESCRIPTION'].apply(lambda x: x[:x.index('(')].strip())
        df['INJURY'] = df['DESCRIPTION'].apply(lambda x: x[x.index('(')+1:x.index(')')].strip())
        df['DESCRIPTION'] = df['DESCRIPTION'].apply(lambda x: x[x.index('-')+2:].strip())
        return df
