import unittest
from basketball_reference_scraper.box_scores import get_box_scores 

class TestBoxScores(unittest.TestCase):
    def test_get_box_scores(self):
        d = get_box_scores('2020-01-06', 'DEN', 'ATL')
        self.assertListEqual(list(d.keys()), ['DEN', 'ATL'])

        df = d['DEN']
        expected_columns = ['Players', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-'] 
        self.assertEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
