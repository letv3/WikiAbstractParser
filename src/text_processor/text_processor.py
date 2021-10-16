# pylucene probably the way to do it
import nltk
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')


class TextProcessor:
    """Class that perform tokenizing , stemming and removing stop words"""
    def __init__(self):
        pass

    def process_text(self, text: str):
        text = self.__tokenize(text)
        text = self.__remove_stop_words(text)
        text = self.__perform_stemming(text)
        return text

    def tokenize(self, text: str) -> list:
        """Tokenizer function"""
        """:return List of words and terms in the text """
        # 'I am the best, today is 4:20 of 12.oct.2021' ->
        #  [I, am, the, best, today, is, 4:20, of, 12.oct.2021
        tokens = nltk.word_tokenize(text)
        return tokens

    def remove_stop_words(self, tokenized_text: list[str]) -> list[str]:
        """remove words like that dont have enough meaning: is, are, am, in, at"""
        # I, am, the, best, today, is, 4:20, of, 12.oct.2021 -> I, best, today, 4:20, 12.oct.2021
        stop_words = set(stopwords.words('english'))
        filtered_sentence = []
        for w in tokenized_text:
            if w not in stop_words:
                filtered_sentence.append(w)
        return filtered_sentence

    def __perform_stemming(self, text: list[str]) -> list[str]:
        """Implement porter stemming algorithm"""
        # https://tartarus.org/martin/PorterStemmer/
        pass

