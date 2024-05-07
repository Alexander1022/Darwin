import sys
sys.path.append('../')
from darwin.comparisons import SpacySimilarity, LevenshteinDistance
import unittest

class TestComparisons(unittest.TestCase):

    def test_SpacySimilarity(self):
        s1 = 'Здравей'
        s2 = 'Здравей'

        spacy_similarity = SpacySimilarity(s1, s2)
        similarity = spacy_similarity.compare()
        self.assertEqual(similarity, 1.0)

    def test_LevenshteinDistance(self):
        s1 = 'Зиги'
        s2 = 'Зигота'

        levenshtein_distance = LevenshteinDistance(s1, s2)
        similarity = levenshtein_distance.compare()
        self.assertEqual(similarity, 0.6)

if __name__ == '__main__':
    unittest.main()
