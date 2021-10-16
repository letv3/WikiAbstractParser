import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityComparator:
    """Class to compare similarity of 2 different(Wiki abstracts in our case)"""

    def __init__(self):
        pass

    def compare_texts(self, first_text: str, second_text: str):
        """function to compare similarity of two texts"""
        """:return Float value from 0 to 1 which represent similarity of two strs"""
        corpus = [first_text, second_text]
        vectorizer = TfidfVectorizer()
        trsfm = vectorizer.fit_transform(corpus)
        pd.DataFrame(trsfm.toarray(), columns=vectorizer.get_feature_names(), index=['first_text', 'second_text'])
        res = cosine_similarity(trsfm[0:1], trsfm).tolist()
        similarity = round(res[0][1],2)
        return similarity
#
# firsr = 'Katia Ndtid'
# sec = 'katia Yulia'
# p = TextSimilarityComparator()
# a = round(p.compare_texts(firsr, sec),2)
#
# print(a)
