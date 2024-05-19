import difflib
import spacy

class LevenshteinDistance:
    def __init__(self, language = 'BG'):
        self.language = language
        
    def compare(self, s1, s2):
        if not s1 or not s2:
            return 0

        s1 = str(s1.lower())
        s2 = str(s2.lower())

        similarity = difflib.SequenceMatcher(None, s1, s2).ratio()
        percent = round(similarity, 2)

        return percent

class SpacySimilarity:
    # using the bulgarian Spacy model created by Ivaylo Sakelariev
    def __init__(self, language = 'bg_news_lg'):
        self.language = language
        
    def compare(self, s1, s2):
        if not s1 or not s2:
            return 0

        nlp = spacy.load(self.language)
        doc1 = nlp(s1)
        doc2 = nlp(s2)

        similarity = doc1.similarity(doc2)

        return similarity

# https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient
class DiceSorensen:
    def __init__(self, language = 'BG'):
        self.language = language

    def compare(self, s1, s2):
        if not s1 or not s2:
            return 0

        s1 = set(s1.split())
        s2 = set(s2.split())

        intersection = len(s1.intersection(s2))
        dice = (2 * intersection) / (len(s1) + len(s2))

        return dice