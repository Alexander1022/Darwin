import sys
sys.path.append('../')
from darwin.search import IndexedTextSearch
import unittest


class TestSearch(unittest.TestCase):
    def test_search(self):
        search = IndexedTextSearch()
        search.texts = ['Здравей', 'Здравейте', 'Как си', 'Как си', 'Как си ти']
        search_results = search.search('Здравейте')
        self.assertEqual(search_results,  [('Здравей', 0.88), ('Здравейте', 1.0)])


if __name__ == '__main__':
    unittest.main()