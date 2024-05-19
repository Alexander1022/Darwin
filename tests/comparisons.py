import sys
sys.path.append('../')
from darwin.comparisons import SpacySimilarity, LevenshteinDistance, DiceSorensen
import unittest

class TestComparisons(unittest.TestCase):

    def test_SpacySimilarity(self):
        s1 = 'Здравей'
        s2 = 'Здравей'

        ss = SpacySimilarity()
        similarity = ss.compare(s1, s2)
        self.assertEqual(similarity, 1.0)

    def test_LevenshteinDistance(self):
        s1 = 'Зиги'
        s2 = 'Зигота'

        ld = LevenshteinDistance()
        similarity = ld.compare(s1, s2)
        self.assertEqual(similarity, 0.6)

    def test_DiceMethod(self):
        s1 = 'България е част от Европа'
        s2 = 'България е в Европа'

        ds = DiceSorensen()
        similarity = ds.compare(s1, s2)
        self.assertAlmostEqual(similarity, 0.6667, places=4)


if __name__ == '__main__':
    unittest.main()
