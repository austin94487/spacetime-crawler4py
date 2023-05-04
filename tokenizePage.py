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

    page_text = soup.get_text()

    # remove punc, replaces with a space
    page_text = re.sub('[\W_]+', ' ', page_text)

    # lowercase
    page_text = page_text.lower()
    
    split_words = page_text.split()

    # I have arbitarily decided that 10000 words is too much
    if len(split_words) > 10000:
        return

    # Potentially update longest page
    if len(split_words) > Database.longest_page[1]:
        Database.longest_page = (url, len(split_words))


    # similar to a for links, p is used in html for paragraphs
    for word in split_words:
        # Decodes characters into English as best as it can
        decodedWord = unidecode(word)
        
        if decodedWord not in StopWords.stop_words:
            
            # "i" is okay
            # "t" is not


            wordLength = len(decodedWord)
            if wordLength > 1:
                word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
            elif wordLength == 1:
                # 105 and 97 are the ord for "i" and "a", the only single letter words in English
                if ord(decodedWord) != 105 and ord(decodedWord) != 97 or decodedWord.isnumeric():
                    word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
            
            # word_map.get(word, 0) returns 0 if key does not exist in the dictionary already
            # https://stackoverflow.com/questions/6130768/return-a-default-value-if-a-dictionary-key-is-not-available for more explanation
'''
def tokenize(url, soup, word_map):

    #I have arbitarily decided that 10000 words is too much
    #print(soup.get_text().split())
    if len(soup.get_text().split()) > 10000:
        return

    # similar to a for links, p is used in html for paragraphs
    for paragraph in soup.find_all('p'):
        paragraphAsString = paragraph.get_text()  # obtain text from paragraphs on webpage

        # remove punc, replaces with a space
        paragraphAsString = re.sub('[\W_]+', ' ', paragraphAsString)

        # lowercase
        paragraphAsString = paragraphAsString.lower()

        # Remove nonenglish, nonnumberic
        # for character in paragraphAsString:
        #    if(ord(character) > 127 or ord(character) < 0):
        #        paragraphAsString = paragraphAsString.replace(character, "")

        # Default splits by whitespace
        wordList = paragraphAsString.split()
        
        # Potentially update longest page
        pageLength = len(wordList)
        if pageLength > Database.longest_page[1]:
            Database.longest_page = (url, pageLength)
            
        for word in wordList:
            
            # Decodes characters into English as best as it can
            decodedWord = unidecode(word)
            
            if decodedWord not in StopWords.stop_words:
                
                
                if len(decodedWord) > 1:
                    word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
                else:
                    # 105 and 97 are the ord for "i" and "a", the only single letter words in English
                    if ord(decodedWord) != 105 and ord(decodedWord) != 97 or decodedWord.isnumeric():
                        word_map[decodedWord] = word_map.get(decodedWord, 0) + 1
                
                # word_map.get(word, 0) returns 0 if key does not exist in the dictionary already
                # https://stackoverflow.com/questions/6130768/return-a-default-value-if-a-dictionary-key-is-not-available for more explanation
'''

def count50(tokenDict):
    # Print by descending order in terms of how many times they are counted
    for key, value in sorted(tokenDict.items(), key=lambda x:-x[1])[0:50]:
        print(key, "-", value)
    
    return 


# function to extract html document from given url
def getHTMLdocument(url):

    response = requests.get(url)

    return response.text


if __name__ == "__main__":

    url1 = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
    url2 = "https://www.crummy.com/software/BeautifulSoup/"

    url3 = "https://www.ics.uci.edu/~kay/wordlist.txt"
    html_document3 = getHTMLdocument(url3)
    soup3 = BeautifulSoup(html_document3, 'html.parser')
    word_map = {}
    tokenize(url3, soup3, word_map)
    print(word_map)
    
    
    '''
    html_document = getHTMLdocument(url1)
    html_document2 = getHTMLdocument(url2)

    soup1 = BeautifulSoup(html_document, 'html.parser')
    soup2 = BeautifulSoup(html_document2, 'html.parser')

    stop_words = StopWords()
    
    totalMap = {}
    try:
        word_map = {}
        tokenize(url1, soup1, word_map)
        tokenize(url2, soup2, word_map)
        totalKeys = set(word_map.keys())
        count50(word_map)

    except Exception as e:
        print("Error occured in tokenize")
        print("Error message:\n", str(e))
    '''