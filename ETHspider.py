# coding=utf-8
from web3 import Web3
import re
import requests
# from multiprocessing import Process, Manager
import threading


ApiKeyToken = '6SG91UUD17M4GCBQJUYY3TKY9B8IP8KVK1'

w3 = Web3(Web3.HTTPProvider("http://192.168.10.210:8545"))

blockstart, blockend= 2103333, 2103338

slice_len = 3

# number = 100
# numlist = list(range(number))
# for i in range(int(number / 3)):
#     for _ in numlist[0:3]:
#         print(_)
#         del numlist[0:3]
#
# print(numlist)

threadLock = threading.RLock()


def get_addr_code(transactions):
    contractaddr = set()
    transactionlist = re.findall("\('(.*?)'\)", str(transactions))
    for i in transactionlist:
        threadLock.acquire()
        content = w3.eth.getTransaction(i)
        try:
            fromaddr = re.search("'from': '(.*?)'", str(content))[1]
            toaddr = re.search("'to': '(.*?)'", str(content))[1]
            if w3.eth.getCode(toaddr)[0:3] != b'':
                contractaddr.add(toaddr)
            if w3.eth.getCode(toaddr)[0:3] != b'':
                contractaddr.add(fromaddr)
        except Exception as e:
            pass
        threadLock.release()

    for addr in contractaddr:
        api = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address=%s&apikey=%s' % (
        addr, ApiKeyToken)
        try:
            res = requests.get(api, timeout=5)
            if eval(res.text)['result'][0]['SourceCode']:
                with open('contract_code.txt', 'a') as f:
                    f.write(addr + ':\r\n' + eval(res.text)['result'][0]['SourceCode'] + '\r\n\r\n')
        except Exception as e:
            pass


def spider(blocklist):
    transactions = []
    # blocklist = list(range(blockstart, blockend))
    threadLock.acquire()
    for i in range(int(len(range(blockstart, blockend)) / 3)):
        threadLock.acquire()
        for block in blocklist[0:slice_len]:
            transactions += (w3.eth.getBlock(block)['transactions'])
        get_addr_code(transactions)
        del blocklist[0:slice_len]
        transactions = []
        threadLock.release()
    threadLock.release()
    for block in blocklist:  # go over the last slice of the blocklist
        transactions += (w3.eth.getBlock(block)['transactions'])
    get_addr_code(transactions)


def multi_thread_scrape(blocklist, thread):

    jobs = []
    for i in range(thread):
        p = threading.Thread(target=spider, args=(blocklist, ))
        jobs.append(p)
        p.start()

    # join threads
    for job in jobs:
        if job.is_alive():
            job.join()


def main():
    # manager = Manager()
    blocklist = list(range(blockstart, blockend))
    multi_thread_scrape(blocklist=blocklist, thread=10)


if __name__ == '__main__':
    main()
