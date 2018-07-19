from multiprocessing import Manager
from ETHspider import multi_thread_scrape

blockstart, blockend = 2103333, 2103338


def test_multiwork():
    manager = Manager()
    blocklist = manager.list(range(blockstart, blockend))
    assert multi_thread_scrape(blocklist=blocklist, thread=20) == 'finished'
