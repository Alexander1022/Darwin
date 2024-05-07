from comparisons import SpacySimilarity, LevenshteinDistance

class IndexedTextSearch:
    def __init__(self, **kwargs):
        statement_comparison_function = kwargs.get('statement_comparison_function', LevenshteinDistance)
        self.compare_statements = statement_comparison_function(language = 'bg_news_lg')


    def search(self, input_text):
        search_results = []

        def_confidence = 0.0

        for text in self.texts:
            confidence = self.compare_statements.compare(input_text, text)
            if confidence > def_confidence:
                def_confidence = confidence
                search_results.append((text, confidence)) 
            
        return search_results