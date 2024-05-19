import spacy 

class PosTagging:
    def __init__(self, language = 'bg_news_lg'):
        self.language = language
        self.punct_table = str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        self.nlp = spacy.load(self.language)

    def tag(self, text):
        without_punct = text.translate(self.punct_table)
        doc = self.nlp(without_punct.lower())

        tokens = [
            token for token in doc if token.is_alpha and not token.is_stop
        ]

        # in case there are no tokens left after filtering
        if(len (tokens) < 2):
            tokens = [
                token for token in doc if token.is_alpha
            ]
    
        pos_pairs = [set([token.text, token.pos_]) for token in tokens]
        return pos_pairs