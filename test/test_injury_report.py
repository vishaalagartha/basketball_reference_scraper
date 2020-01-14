import unittest
from basketball_reference_scraper.injury_report import get_injury_report

class TestInjuryReport(unittest.TestCase):
    def test_injury_report(self):
        df = get_injury_report()
        expected_columns = ['PLAYER', 'TEAM', 'DATE', 'INJURY', 'STATUS', 'DESCRIPTION']
        self.assertCountEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
