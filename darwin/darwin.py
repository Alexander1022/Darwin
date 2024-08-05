from training import Trainer
from chatbot import Darwin

trainer = Trainer()
trainer.train_model()

darwin = Darwin()
darwin.start()