import random
import json
import pickle
import numpy as np
from simplemma import lemmatize, simple_tokenizer
from tensorflow.keras.models import load_model
from context_parser import ContextParser

class Darwin:
    def __init__(self, intents_path='../additional/intents.json', classes_path = '../additional/classes.pkl', words_path='../additional/words.pkl', model_path='darwin_model.h5'):
        self.intents = json.loads(open(intents_path, encoding='utf-8').read())
        self.words = pickle.load(open(words_path, 'rb'))
        self.classes = pickle.load(open(classes_path, 'rb'))
        self.model = load_model(model_path)
        self.context_parser = ContextParser()

    def clean_up_sentence(self, sentence):
        sentence_words = simple_tokenizer(sentence)
        sentence_words = [lemmatize(word, lang='bg') for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for word in sentence_words:
            for i, w in enumerate(self.words):
                if w == word:
                    bag[i] = 1

        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.5
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = [{'intent': self.classes[r[0]], 'probability': str(r[1])} for r in results]
        print(return_list)

        return return_list

    def get_response(self, intents_list):
        if not intents_list:
            return 'Извинете, не разбрах.'
            
        tag = intents_list[0]['intent']
        for intent in self.intents['intents']:
            if intent['tag'] == tag:
                if 'context' in intent:
                    print('Има контекст')
                    return self.context_parser.parse(intent['context'])     
                return random.choice(intent['responses'])

        return 'Извинете, не разбрах.'

    def start(self):
        while True:
            message = input("")
            intents_list = self.predict_class(message)
            result = self.get_response(intents_list)
            print(result)
