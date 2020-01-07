import unittest
from basketball_reference_scraper.players import get_stats

class TestPlayers(unittest.TestCase):
    def test_get_stats(self):
        df = get_stats('LaMarcus Aldridge') 
        expected_columns = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        self.assertListEqual(list(df.columns), expected_columns)

        df = get_stats('LaMarcus Aldridge', career=True)
        expected_columns = ['Season', 'Tm', 'Lg', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        self.assertListEqual(list(df.columns), expected_columns)

        df = get_stats('LaMarcus Aldridge', playoffs=True, career=True)
        expected_columns = ['Season', 'Tm', 'Lg', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        self.assertListEqual(list(df.columns), expected_columns)


if __name__ == '__main__':
    unittest.main()
