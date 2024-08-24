import random
import json
import pickle
import numpy as np

from simplemma import simple_tokenizer
from simplemma import lemmatize
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

class Trainer:
    def __init__(self, intents_path = '../additional/intents.json'):
        self.intents_path = intents_path
        self.intents = []
        self.words = []
        self.classes = []
        self.documents = []
        self.training = []
        self.ignore_letters = ['!', '?', ',', '.']
        self.load_intents()
        self.prepare_data()

    def load_intents(self):
        with open(self.intents_path, encoding='utf-8') as file:
            self.intents = json.load(file)

    def prepare_data(self):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word_list = simple_tokenizer(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [lemmatize(word, lang='bg') for word in self.words if word not in self.ignore_letters]
        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))

        pickle.dump(self.words, open('../additional/words.pkl', 'wb'))
        pickle.dump(self.classes, open('../additional/classes.pkl', 'wb'))

        output_empty = [0] * len(self.classes)

        for document in self.documents:
            bag = []
            word_patterns = document[0]
            word_patterns = [lemmatize(word.lower(), lang='bg') for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(document[1])] = 1
            self.training.append([bag, output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)

        self.train_x = list(self.training[:, 0])
        self.train_y = list(self.training[:, 1])

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.train_y[0]), activation='softmax'))

        sgd = SGD(learning_rate = 0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        
        return model

    def train_model(self, epochs=200, batch_size=5, file_name = 'darwin_model.h5'):
        model = self.build_model()
        hist = model.fit(np.array(self.train_x), np.array(self.train_y), epochs=epochs, batch_size=batch_size, verbose=1)
        model.save(file_name, hist)
        print('Model created!')
