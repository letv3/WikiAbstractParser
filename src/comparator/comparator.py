from sklearn.metrics.pairwise import cosine_similarity
from text_processor.text_processor import TextProcessor
from sklearn.feature_extraction.text import CountVectorizer



class TextSimilarityComparator:
    """Class to compare similarity of 2 different(Wiki abstracts in our case)"""

    def __init__(self):
        pass

    def compare_texts(self, first_text: str, second_text: str):
        """function to compare similarity of two texts"""
        """:return Float value from 0 to 1 which represent similarity of two strs"""
        d = TextProcessor()
        text = []
        # clean text
        t1 = d.process_text(text=first_text)
        t2 = d.process_text(text=second_text)
        # concatenate words and add them to the one list
        t1 = ' '.join(map(str, t1))
        t2 = ' '.join(map(str, t2))
        text.append(t1)
        text.append(t2)
        # convert the data into vectors
        vectorizer = CountVectorizer()
        vectorizer.fit(text)
        vectors = vectorizer.transform(text).toarray()
        # cos_sim is a diagonal matrix 2x2, take one element
        cos_sim = cosine_similarity(vectors)
        similarity = round(cos_sim[0][1], 2)
        return similarity
