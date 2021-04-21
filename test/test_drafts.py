import unittest
from basketball_reference_scraper.drafts import get_draft_class

class TestDraft(unittest.TestCase):

  def test_should_get_class(self):
    df = get_draft_class(2003)
    self.assertEqual(len(df), 58)

    row = df.iloc[0]
    self.assertEqual('LeBron James', row['PLAYER'])

  def test_should_get_old_class(self):
    df = get_draft_class(1987)
    self.assertEqual(len(df), 161)

  def test_should_handle_forfeit(self):
    df = get_draft_class(2002)
    self.assertEqual(len(df), 57)

    row = df.iloc[27]
    self.assertEqual('28', row['PICK'])
    row = df.iloc[28]
    self.assertEqual('30', row['PICK'])