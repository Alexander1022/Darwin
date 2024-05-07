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