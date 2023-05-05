import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from crawler.database import Database
from utils.stopwords import StopWords
import tokenizePage

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
    url = url.partition("#")[0]  # checks for a fragment and strips it from the url. Placed before checking for duplicates so we don't include the fragment. 

    if (response.status != 200) or (url in Database.scraped):
        # detect redirects, add new url to url_list to be scraped
        if response.status >= 300 and response.status < 400 and response.raw_response.url != response.url: 
            url_list.append(response.raw_response.url) 
            Database.redirects_links += 1
        else:
            return []
        
    soup = BeautifulSoup(response.raw_response.content, "lxml")
    
    # detect and avoid dead urls that return 200 status but no data 
    if (len(soup.find_all("a")) == 0 and len(soup.find_all("body")) < 100): 
        # no links on page and low information = dead page
        Database.dead_links += 1
        return []

    for link in soup.find_all('a'): 
        # finding links and adding them to the list
        href_link = link.get('href')
        url_list.append(href_link)


    # Decided arbitarily 0 is small enough
    if len(url_list) > 0:
        tokenizePage.tokenize(url, soup, Database.total_map)
        Database.scraped.add(url)
        parsed = urlparse(url)
        Database.unique_urls.add(parsed.netloc)

    return url_list


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        # did we scrape it already? we dont need to crawl it again.
        if url in Database.scraped:
            return False
        
        parsed = urlparse(url)
        # Check for http protocol 
        if parsed.scheme not in set(["http", "https"]):
            return False
        

        # Checking if school website        
        #if "ics.uci.edu" not in parsed.netloc and "cs.uci.edu" not in parsed.netloc and "informatics.uci.edu" not in parsed.netloc and "stat.uci.edu" not in parsed.netloc:
        #   return False
        
        if parsed.netloc != "ics.uci.edu" and parsed.netloc != "cs.uci.edu" and parsed.netloc != "informatic.uci.edu" and parsed.netloc != "stat.uci.edu":
            # first, check if its the base site. if it falls into any one of the base subdomains, it moves on. 
            if ".ics.uci.edu" not in parsed.netloc and ".cs.uci.edu" not in parsed.netloc and ".informatics.uci.edu" not in parsed.netloc and ".stat.uci.edu" not in parsed.netloc:
                # filters out econimics.uci.edu by including the .
                return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            +r"|png|tiff?|mid|mp2|mp3|mp4"
            +r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            +r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            +r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            +r"|epub|dll|cnf|tgz|sha1"
            +r"|thmx|mso|arff|rtf|jar|csv|r"
            +r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        # Avoid links with repeating directories
        # https://support.archive-it.org/hc/en-us/articles/208332963-How-to-modify-your-crawl-scope-with-a-regular-expression
        if re.match(r"^.*?(\/.+?\/).*?\1.*$|^.*?\/(.+?\/)\2.*$", parsed.path.lower()):
            return False


        if ".ics.uci.edu" in parsed.netloc and "ics.uci.edu" != parsed.netloc:
            httpWithNetloc = parsed.scheme + "://" + parsed.netloc
            Database.subdomains[httpWithNetloc] = Database.subdomains.get(parsed.scheme + "://" + parsed.netloc, 0) + 1
            
            tempURL = parsed.netloc
            tempURL = tempURL.replace("www.","")

            Database.url_to_subdomain[httpWithNetloc] = tempURL
         
        return True
        
    except TypeError:
        return False
