import unittest
from basketball_reference_scraper.teams import get_roster, get_team_series, get_opp_series, get_roster_stats, get_team_misc, get_player_salaries 

class TestTeams(unittest.TestCase):
    def test_get_roster(self):
        df = get_roster('GSW', 2019)
        curry_df = df[df['PLAYER']=='Stephen Curry']
        self.assertEqual(len(curry_df), 1)

        expected_columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT',
                'BIRTH_DATE', 'NATIONALITY', 'EXPERIENCE', 'COLLEGE']

        self.assertListEqual(list(df.columns), expected_columns) 

    def test_get_team_series(self):
        series = get_team_series('GSW', 2019)
        expected_indices = ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        self.assertListEqual(list(series.index), expected_indices)

    def test_get_opp_series(self):
        series = get_opp_series('GSW', 2019)
        expected_indices = ['OPP_G', 'OPP_MP', 'OPP_FG', 'OPP_FGA', 'OPP_FG%', 'OPP_3P', 'OPP_3PA', 'OPP_3P%', 'OPP_2P', 'OPP_2PA', 'OPP_2P%', 'OPP_FT', 'OPP_FTA', 'OPP_FT%', 'OPP_ORB', 'OPP_DRB', 'OPP_TRB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV', 'OPP_PF', 'OPP_PTS']
        self.assertListEqual(list(series.index), expected_indices)

    def test_get_roster_stats(self):
        df = get_roster_stats('GSW', 2019, data_format='ADVANCED', playoffs=True)
        expected_columns = ['Name', 'Age', 'G', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']
        self.assertListEqual(list(df.columns), expected_columns)

    def test_get_team_misc(self):
        series = get_team_misc('GSW', 2019)
        expected_indices = ['W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', 'Arena', 'Attendance']

        self.assertListEqual(list(series.index), expected_indices)


    def test_player_salaries(self):
        df = get_player_salaries('GSW', 2019) 
        expected_columns = ['NAME', 'SALARY']
        self.assertListEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
