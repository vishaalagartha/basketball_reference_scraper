import unittest
from basketball_reference_scraper.box_scores import get_box_scores, get_all_star_box_score 

class TestBoxScores(unittest.TestCase):
    def test_get_box_scores(self):
        d = get_box_scores('2020-01-06', 'DEN', 'ATL')
        self.assertListEqual(list(d.keys()), ['DEN', 'ATL'])

        df = d['DEN']
        expected_columns = ['PLAYER', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-']
        self.assertListEqual(list(df.columns), expected_columns)

    def test_get_all_star_box_score(self):
        d = get_all_star_box_score(2020)
        df = d['Team LeBron']
        # they dont record +/- in ASG :(
        expected_columns = ['PLAYER', 'TEAM', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
        for item in df.columns:
            if item not in expected_columns:
                print(item) 
        self.assertSetEqual(set(df.columns), set(expected_columns))

        # check for one of the dnp players
        self.assertTrue('Damian Lillard' in df['PLAYER'].values)
        d2 = get_all_star_box_score(1980)
        df = d2['East']
        # check uniqueness of all star names
        expected_players = ['George Gervin', 'Eddie Johnson', 'Moses Malone', 'Julius Erving', 'John Drew', 'Elvin Hayes', 'Dan Roundfield', 'Larry Bird', 'Tiny Archibald', 'Bill Cartwright', 'Micheal Ray Richardson', 'Dave Cowens']
        self.assertListEqual(expected_players, list(df['PLAYER'].values))

if __name__ == '__main__':
    unittest.main()
