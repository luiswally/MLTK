import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Sentiment:
    # Constructor method of Sentiment
    def __init__(self, tempInput):
        self.tempInput = tempInput
        self.tempInternalField = None
        self.foo() # set internal field to whatever it needs to be via foo()

    
    # implement Vader out-of-box sentiment analyzer then try training or hardcoding emojis for positive
    def foo(self):
        pass

    
    

