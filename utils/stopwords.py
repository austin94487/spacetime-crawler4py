import sys

class StopWords:
    stop_words = set()

    def __init__(self):
        stop_words = set() 
        with open("stopwords.txt") as f:
            for word in f.read():
                self.stop_words.add(word)
    
    def contains(word):
        return word in self.stop_words