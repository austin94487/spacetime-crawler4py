class Database:
    unique_urls = set()
    scraped = set()
    total_map = {}
    longest_page = ("", 0)  # string is a URL, 0 is total words.
    dead_links = 0
    redirects_links = 0 
    subdomains = {}
    url_to_subdomain = {}



def __init__(self):
    self.unique_urls = set()
    self.scraped = set()
    self.total_map = {}
    self.longest_page = ("", 0)
    self.dead_links = 0
    self.redirects_links = 0
    self.subdomains = {}
    self.url_to_subdomain = {}
    # Should this be a static variable?
    # self.longest_page = ("", 0)
