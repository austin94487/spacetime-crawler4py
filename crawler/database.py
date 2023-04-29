class Database:
    unique_urls = set()
    scraped = set()
    total_map = {}
    longest_page = ("", 0)  # string is a URL, 0 is total words.


def __init__(self):
    self.unique_urls = set()
    self.scraped = set()
    self.total_map = {}
    
    # Should this be a static variable?
    # self.longest_page = ("", 0)
