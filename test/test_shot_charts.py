import unittest
from basketball_reference_scraper.shot_charts import get_shot_chart

class TestShotCharts(unittest.TestCase):
    def test_get_shot_chart(self):
        d = get_shot_chart('2019-12-28', 'TOR', 'BOS')
        self.assertListEqual(list(d.keys()), ['TOR', 'BOS'])
        self.assertListEqual(list(d['TOR'].columns), ['x', 'y', 'QUARTER', 'TIME_REMAINING', 'PLAYER', 'MAKE_MISS', 'VALUE', 'DISTANCE'])
if __name__ == '__main__':
    unittest.main()
