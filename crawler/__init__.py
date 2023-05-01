from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker

class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier, worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory

    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()

    def start(self):
        self.start_async()
        self.join()

    def join(self):
        for worker in self.workers:
            worker.join()







'''
# 1. Import the library
import concurrent.futures

# 2. Define the function
def our_function(data):
	# Fill with code

# 3. Run the multithreading (You can apply any number of max worker)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
	executor.map(our_function, list_of_data)


'''

