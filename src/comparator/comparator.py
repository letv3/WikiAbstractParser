import string, re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords


class TextSimilarityComparator:
    """Class to compare similarity of 2 different(Wiki abstracts in our case)"""

    def __init__(self):
        try:
            self.stopwords = stopwords.words('english')
        except:
            nltk.download('stopwords')
            self.stopwords = stopwords.words('english')

    def clean_string(self, text):
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in self.stopwords])
        return text

    def compare_texts(self, first_text, second_text) -> float:
        """function to compare similarity of two texts"""
        """:return Float value from 0 to 1 which represent similarity of two strs"""
        if first_text == None or first_text == '' \
            or second_text == None or second_text == '':
            return 0.0
        cleaned = list(map(self.clean_string, [first_text, second_text]))
        for cleaned_str in cleaned:
            if not cleaned_str or len(re.sub(r"\s+", "", cleaned_str)) < 3:
                return 0.0
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        first_text = vectors[0].reshape(1, -1)
        second_text = vectors[1].reshape(1, -1)
        return float(cosine_similarity(first_text, second_text)[0][0])


if __name__ == '__main__':
    comparator = TextSimilarityComparator()

    va = 'a an in'

    vb = "stop motion animation used describe animation created physically " \
         "manipulating real world objects photographing them one frame film time create illusion "

    csim = comparator.compare_texts(va, vb)
    print(csim)
    print(type(csim))
