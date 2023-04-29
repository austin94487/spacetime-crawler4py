# import necessary libraries
from bs4 import BeautifulSoup
import requests
import re
  
  
# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
      
    # response will be provided in JSON format
    return response.text



url_to_scrape = "https://www.crummy.com/software/BeautifulSoup/bs4/doc/"



  
html_document = getHTMLdocument(url_to_scrape)

soup = BeautifulSoup(html_document, 'html.parser')
  


someSet= set()
anotherSet = set()


for link in soup.find_all('a', attrs={'href': re.compile("^https://")}): 
    someSet.add(link.get('href'))


for item in someSet:
    print(item)

exit()


for url in someSet:

    #expanding the lsit of visited pages
    url_to_scrape = url
    html_document = getHTMLdocument(url_to_scrape)
    soup = BeautifulSoup(html_document, 'html.parser')

    for link in soup.find_all('a', attrs={'href': re.compile("^https://")}):
        anotherSet.add(link.get('href'))

print(len(someSet))
print(len(anotherSet))



setOfAllSets = someSet.union(anotherSet)

# for item in setOfAllSets:
#    print(item)

print("ending program")