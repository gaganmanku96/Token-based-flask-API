import re

from textblob import TextBlob


class Model:
    def __init__(self):
        pass

    def _preprocess(self, sentence: str) -> str:
        return sentence.lower()

    def predict(self, sentence:str) -> str:
        result = {}
        processed_sentence = self._preprocess(sentence)
        polarity, _ = TextBlob(processed_sentence).sentiment
        if polarity < 0:
            result['sentiment'] = 0
        else:
            result['sentiment'] = 1
        return result
