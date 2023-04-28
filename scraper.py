import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.urlstore import URLStore
from utils.stopwords import StopWords

# The scraper function receives a URL and corresponding Web response 
# (for example, the first one will be "http://www.ics.uci.edu" and 
# the Web response will contain the page itself). Your task is to parse 
# the Web response, extract enough information from the page 
# (if it's a valid page) so as to be able to answer the questions for the report, 
# and finally, return the list of URLs "scrapped" from that page.

# ARGS
# url: The URL that was added to the frontier, and downloaded from the cache. It is of type str and was an url that was previously added to the frontier.
# resp:
# This is the response given by the caching server for the requested URL. The response is an object of type Response (see utils/response.py)

def scraper(url, response):
    links = extract_next_links(url, response)
    url_list = [link for link in links if is_valid(link)]
    return url_list


def extract_next_links(url, response):


    # Implementation required.
    # url: the URL that was used to get the page
    # response.url: the actual url of the page
    # response.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # response.error: when status is not 200, you can check the error here, if needed.
    # response.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         response.raw_response.url: the url, again
    #         response.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from response.raw_response.content


    url_list = []
    print("running extract_next_links")

    if (response.status != 200) or (url in URLStore.scraped):
        print(f"Error: {response.status}")
        # empty return
        return []
        
        

    soup = BeautifulSoup(response.raw_response.content, "lxml")

    
    #soup = BeautifulSoup(response.raw_response.content, 'html.parser')
    #print(soup.prettify())

    for link in soup.find_all('a'):
        # might want to check validity of the link
        href_link = link.get('href')
        if is_valid(href_link):
            #print(link.get('href'))
            url_list.append(href_link)
    # NEED TO GET EVERYTHING IN THE FORMAAT <href="somestring">

    # tofix?
    URLStore.scraped.add(url)
    return url_list

def is_valid(url):

    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        

        # Check for http protocol 
        if parsed.scheme not in set(["http", "https"]):
            return False

        # Checking if school website        
        #print("netloc: ", parsed.netloc)
        
        
        if "ics.uci.edu" not in parsed.netloc and "cs.uci.edu" not in parsed.netloc and "informatics.uci.edu" not in parsed.netloc and "stat.uci.edu" not in parsed.netloc:
            # print("not valid:", parsed.netloc)
            return False

        # print(parsed.netloc)    
        #if not re.match(r'(ics.uci.edu|cs.uci.edu|informatics.uci.edu|stat.uci.edu)', parsed.netloc):
        # if parsed.netloc not in set(['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']):
        
            #return False
 
        '''
        Some notable netlocs

        netloc:  mhcid.ics.uci.edu
        netloc:  mse.ics.uci.edu
        netloc:  www.facebook.com
        netloc:  twitter.com
        netloc:  uci.edu
        netloc:  recruit.ap.uci.edu
        netloc:  intranet.ics.uci.edu
        ''' 

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        if parsed.netloc not in URLStore.unique_urls: 
            URLStore.unique_urls.add(parsed.netloc) 
        return True



    except TypeError:
        print ("TypeError for ", parsed)


        return False
