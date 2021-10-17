import unittest
from comparator.comparator import TextSimilarityComparator


class TestComparator(unittest.TestCase):

    def setUp(self) -> None:
        self.comparator = TextSimilarityComparator()

    def test_same_texts(self):
        text_1 = 'Apple is green'
        text_2 = 'Apple is green'
        expected_result = 1.0
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Should be 100% similarity")

    def test_tot_diff_texts(self):
        text_1 = 'Azure currently supports SSH protocol'
        text_2 = 'Yesterday I ate two apples'
        expected_result = 0
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Should be 0 similarity")

    def test_slightly_diff_texts(self):
        text_1 = 'An apple is yellow'
        text_2 = 'An apple is not green'
        expected_result = 0.67
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Similarity should be high enough")

    def test_slightly_sim_texts(self):
        text_1 = 'I like apples, but not oranges'
        text_2 = 'I like oranges, but not oranges'
        expected_result = 0.77
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Similarity should be high enough")

    def test_diff_context_texts(self):
        text_1 = 'Apple is a fruit'
        text_2 = 'I like berries, but not oranges'
        expected_result = 0
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Similarity should be very low")

    def test_diff_meaning_texts(self):
        text_1 = 'Apple is my favorite fruit!'
        text_2 = 'I hate apples'
        expected_result = 0
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Similarity should be very low")

    def test_sim_meaning_texts(self):
        text_1 = 'I like apples and berries!'
        text_2 = 'I prefer apples rather than berries'
        expected_result = 0.58
        p = self.comparator
        actual_similarity = p.compare_texts(text_1, text_2)
        self.assertEqual(actual_similarity, expected_result, "Similarity should be high enough")


if __name__ == '__main__':
    unittest.main()
