from multiprocessing import Manager
import os
from ..ETHspider import multi_thread_scrape

blockstart, blockend = 2103333, 2103338


def test_multiwork():
    print(os.getcwd())
    manager = Manager()
    blocklist = manager.list(range(blockstart, blockend))
    assert multi_thread_scrape(blocklist=blocklist, thread=20) == 'finished'
