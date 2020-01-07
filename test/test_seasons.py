import unittest
from basketball_reference_scraper.seasons import get_schedule, get_standings 

class TestSeason(unittest.TestCase):
    def test_get_schedule(self):
        df = get_schedule(1999)
        expected_columns = ['Date', 'Visitor', 'Visitor Pts', 'Home', 'Home Pts', 'Attendance']
        self.assertListEqual(list(df.columns), expected_columns)

    def test_get_standings(self):
        d = get_standings()
        self.assertListEqual(list(d.keys()), ['Eastern Conference', 'Western Conference'])

        df = d['Western Conference']
        expected_columns = ['Western Conference', 'W', 'L', 'W/L%', 'GB', 'PW', 'PL', 'PS/G', 'PA/G']
        self.assertListEqual(list(df.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
