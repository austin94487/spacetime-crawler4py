import sys

class StopWords:
    stop_words = set()

    def __init__(self):
        stop_words = set() 
        with open("stopwords.txt", 'r') as f:
            for word in f:
                self.stop_words.add(word.strip("\n"))
            
    
    def contains(word):
        return word in self.stop_words