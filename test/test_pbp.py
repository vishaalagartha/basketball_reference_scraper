import unittest
from basketball_reference_scraper.pbp import get_pbp

class TestPbp(unittest.TestCase):
    def test_pbp(self):
        df = get_pbp('2020-01-06', 'DEN', 'ATL')
        expected_columns = ['Clock', 'Denver', 'Atlanta', 'Denver Score', 'Atlanta Score']
        self.assertListEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
