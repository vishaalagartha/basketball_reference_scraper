import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def get_draft_class(year):
      r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fdraft%2FNBA_{year}.html&div=div_stats')
      df = None

      if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]

        # get rid of duplicate pick col
        df.drop(['Unnamed: 0_level_0'], inplace=True, axis = 1, level=0)
        df.rename(columns={'Unnamed: 1_level_0': '', 'Pk': 'PICK', 'Unnamed: 2_level_0': '', 'Tm': 'TEAM',
                  'Unnamed: 5_level_0': '', 'Yrs': 'YEARS', 'Totals': 'TOTALS', 'Shooting': 'SHOOTING',
                  'Per Game': 'PER_GAME', 'Advanced': 'ADVANCED', 'Round 1': '', 
                  'Player': 'PLAYER', 'College': 'COLLEGE'}, inplace=True)

        # flatten columns
        df.columns = ['_'.join(x) if x[0] != '' else x[1] for x in df.columns]

        # remove mid-table header rows
        df = df[df['PLAYER'].notna()]
        df = df[~df['PLAYER'].str.contains('Round|Player')]

        return df
