import re
import requests
from bs4 import BeautifulSoup
import json
# from utils.s import StopWords
from utils.stopwords import StopWords
import time
from crawler.database import Database
from unidecode import unidecode

def tokenize(url, soup, word_map):

    print("1 ERROR CHECK TKNZ", url)
    page_text = soup.get_text()

    # remove punc, replaces with a space
    page_text = re.sub("-|'", '', page_text)
    page_text = re.sub('[\W_]+', ' ', page_text)
    
    # lowercase
    page_text = page_text.lower()
    
    split_words = page_text.split()

    # I have arbitarily decided that 10000 words is too much
    split_words_length = len(split_words)
    if split_words_length > 10000:
        return

    print("2 ERROR CHECK TKNZ", url, "should be less than 10000", len(split_words))
    # Potentially update longest page
    if split_words_length > Database.longest_page[1]:
        Database.longest_page = (url, split_words_length)


    # similar to a for links, p is used in html for paragraphs
    for word in split_words:
        # Decodes characters into English as best as it can
        decodedWord = unidecode(word)
        
        if decodedWord not in StopWords.stop_words:

            wordLength = len(decodedWord)
            if wordLength > 1:
                word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
            elif wordLength == 1:
                # 105 and 97 are the ord for "i" and "a", the only single letter words in English
                if (ord(decodedWord) == 105 or ord(decodedWord) == 97):
                    word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
            
            # word_map.get(word, 0) returns 0 if key does not exist in the dictionary already
            # https://stackoverflow.com/questions/6130768/return-a-default-value-if-a-dictionary-key-is-not-available for more explanation
    
    print("3 ERROR CHECK TKNZ", url)

def count50(tokenDict):
    # Print by descending order in terms of how many times they are counted
    i = 1
    for key, value in sorted(tokenDict.items(), key=lambda x:-x[1])[0:50]:
        print(i,":",key, "-", value)
        i+=1
    return 


# function to extract html document from given url
def getHTMLdocument(url):
    response = requests.get(url)
    return response.text


