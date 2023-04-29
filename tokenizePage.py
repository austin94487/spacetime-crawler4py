import re
import requests
from bs4 import BeautifulSoup
import json
# from utils.s import StopWords
from utils.stopwords import StopWords
import time
from crawler.database import Database

# def tokenize(someSoup, word_map):
def tokenize(url, soup, word_map):
    #start_time = time.time()
    #html_url = getHTMLdocument(url)
    #end_time = time.time()
    #print("Time taken: ", end_time-start_time)

    #soup = BeautifulSoup(html_url, 'lxml')

    # similar to a for links, p is used in html for paragraphs
    for paragraph in soup.find_all('p'):
        paragraphAsString = paragraph.get_text() # obtain text from paragraphs on webpage
        #for word in p.split(' '):

        #remove punc, replaces with a space
        paragraphAsString = re.sub('[\W_]+', ' ', paragraphAsString)

        #lowercase
        paragraphAsString = paragraphAsString.lower()

        #remove nonenglish, nonnumberic
        #for character in paragraphAsString:
        #    if(ord(character) > 127 or ord(character) < 0):
        #        paragraphAsString = paragraphAsString.replace(character, "")
        wordList = paragraphAsString.split()
        if len(wordList) > Database.longest_page[1]:
            Database.longest_page = (url, len(wordList))
        for word in wordList:
            # StopWords is an object, it has a stop_words attribute
            # TODO: Stopwords are making it into the output file, the word "the" is supposably part of the stopwords, and appears as the most commonly used word
            if word not in StopWords.stop_words:
                # word_map.get(word, 0) returns 0 if key does not exist in the dictionary already
                # https://stackoverflow.com/questions/6130768/return-a-default-value-if-a-dictionary-key-is-not-available for more explanation
                word_map[word] = word_map.get(word, 0) + 1

def count50(tokenDict):
    # Print by descending order in terms of how many times they are counted
    for key, value in sorted(tokenDict.items(), key=lambda x: -x[1])[0:50]:
        print(key, "-", value)
    
    return 

# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    # start_time = time.time()
    response = requests.get(url)
    # end_time = time.time()
    # print("Time taken: ", end_time-start_time)
    # response will be provided in JSON format
    return response.text

if __name__ == "__main__":

    url1 = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
    url2 = "https://www.crummy.com/software/BeautifulSoup/"
    
    html_document = getHTMLdocument(url1)
    html_document2 = getHTMLdocument(url2)

    soup1 = BeautifulSoup(html_document, 'html.parser')
    soup2 = BeautifulSoup(html_document2, 'html.parser')

    stop_words = StopWords()
    
    totalMap = {}
    try:
        word_map = {}
        tokenize(soup1, word_map)
        tokenize(soup2, word_map)
        totalKeys = set(word_map.keys())
        count50(word_map)


    except Exception as e:
        print("Error occured in tokenize")
        print("Error message:\n", str(e))