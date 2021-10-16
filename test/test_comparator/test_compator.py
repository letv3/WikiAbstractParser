import unittest
from comparator.comparator import TextSimilarityComparator


class TestCompator(unittest.TestCase):

    def setUp(self) -> None:
        self.compratator = TextSimilarityComparator()

    def test_same_texts(self):
        text_1 = 'Apple is green'
        text_2 = 'Apple is green'
        expected_result = 1.0
        p = self.compratator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result)

    def test_tot_diff_texts(self):
        text_1 = 'Vovolo'
        text_2 = 'Katia'
        expected_result = 0
        p = self.compratator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result)

if __name__ == '__main__':
    unittest.main()
