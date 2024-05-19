import sys
sys.path.append('../')
from darwin.comparisons import SpacySimilarity, LevenshteinDistance
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

if __name__ == '__main__':
    unittest.main()
