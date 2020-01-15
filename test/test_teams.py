import unittest
from basketball_reference_scraper.teams import get_roster, get_team_stats, get_opp_stats, get_roster_stats, get_team_misc

class TestTeams(unittest.TestCase):
    def test_get_roster(self):
        df = get_roster('GSW', 2019)
        curry_df = df[df['PLAYER']=='Stephen Curry']
        self.assertEqual(len(curry_df), 1)

        expected_columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT',
                'BIRTH_DATE', 'NATIONALITY', 'EXPERIENCE', 'COLLEGE']

        self.assertListEqual(list(df.columns), expected_columns) 

    def get_team_stats(self):
        series = get_team_stats('GSW', 2019)
        expected_indices = ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        self.assertCountEqual(list(series.index), expected_indices)

    def get_opp_stats(self):
        series = get_opp_stats('GSW', 2019)
        expected_indices = ['OPP_G', 'OPP_MP', 'OPP_FG', 'OPP_FGA', 'OPP_FG%', 'OPP_3P', 'OPP_3PA', 'OPP_3P%', 'OPP_2P', 'OPP_2PA', 'OPP_2P%', 'OPP_FT', 'OPP_FTA', 'OPP_FT%', 'OPP_ORB', 'OPP_DRB', 'OPP_TRB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV', 'OPP_PF', 'OPP_PTS']
        self.assertCountEqual(list(series.index), expected_indices)

    def test_get_roster_stats(self):
        df = get_roster_stats('GSW', 2019)
        expected_columns = ['PLAYER', 'POS', 'AGE', 'TEAM', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'SEASON']
        self.assertCountEqual(list(df.columns), expected_columns)

    def test_get_team_misc(self):
        series = get_team_misc('GSW', 2019)
        expected_indices = ['AGE', 'W', 'L', 'PW', 'PL', 'MOV', 'SOS', 'SRS', 'ORtg', 'DRtg', 'NRtg', 'PACE', 'FTr', '3PAr', 'TS%', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'eFG%', 'TOV%', 'DRB%', 'FT/FGA', 'ARENA', 'ATTENDANCE', 'ATTENDANCE/G', 'TEAM', 'SEASON']
        self.assertCountEqual(list(series.index), expected_indices)

        series = get_team_misc('CHO', 2019)
        self.assertCountEqual(list(series.index), expected_indices)

        series = get_team_misc('NOK', 2007)
        self.assertCountEqual(list(series.index), expected_indices)

        series = get_team_misc('TCB', 1951)
        self.assertCountEqual(list(series.index), expected_indices)

if __name__ == '__main__':
    unittest.main()
