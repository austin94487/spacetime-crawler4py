from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
from crawler.database import Database


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        data = Database()

        # multithread here?
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            # potentially multithreading goes here
            # idea: there are 4 threads, each for a domain. we put politeness for each
            # best case, each thread has equal number of work to do
            # worst case, it's all one domain
            # no good idea atm to address this
            
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
 
        print("worker")
        print("TOP 50 WORDS")
        for key, value in sorted(data.total_map.items(), key=lambda x: -x[1])[0:50]:
            print(key, "-", value)
        print("UNIQUE NETLOCS")
        for netloc in data.unique_urls:
            print(netloc)
        
        print("Total Map Size: ", len(data.total_map))
        print("Total Unique URLS:", len(data.scraped))
        print("Longest page: ", data.longest_page)

        print("Subdomains Ranked")
        for key, value in sorted(Database.subdomains.items(), key=lambda x: Database.url_to_subdomain.get((x[0]))):
            print(key + ",", str(value))