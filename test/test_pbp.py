import unittest
from basketball_reference_scraper.pbp import get_pbp

class TestPbp(unittest.TestCase):
    def test_pbp(self):
        df = get_pbp('2020-01-06', 'DEN', 'ATL')
        expected_columns = ['QUARTER', 'TIME_REMAINING', 'DENVER_ACTION', 'ATLANTA_ACTION', 'DENVER_SCORE', 'ATLANTA_SCORE']
        self.assertListEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
