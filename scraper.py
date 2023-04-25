import re
from urllib.parse import urlparse

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
    return [link for link in links if is_valid(link)]

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

    '''
    An example of printing the text on a given URL, with all the html formatting, probably not needed because all the information looks like it's already here
    Source: https://realpython.com/beautiful-soup-web-scraper-python/#scrape-the-fake-python-job-site

    import requests

    URL = "https://realpython.github.io/fake-jobs/"
    page = requests.get(URL)

    print(page.text)

    response.raw_response.content

    '''
    


    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]) or parsed.hostname not in set(['ics.uci.edu', 'cs.uci.edu', 'informatics.uci.edu', 'stat.uci.edu']):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)


        raise
