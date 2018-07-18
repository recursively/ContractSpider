# coding=utf-8
from email.mime.multipart import MIMEMultipart
import smtplib
from web3 import Web3
import re
import requests
from multiprocessing import Process, Manager, RLock
# import threading
import pymongo


ApiKeyToken = '6SG91UUD17M4GCBQJUYY3TKY9B8IP8KVK1'

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/po1MoDRgjDD0EPchxiOS"))

blockstart, blockend= 2103333, 2103338

slice_len = 3

address_set = set()  # This set is created to filter the repeated addresses

# threadLock = threading.RLock()

processLock = RLock()

client = pymongo.MongoClient("mongodb://%s:%s@192.168.10.220" % ('root', 'ATWtGZhsP4FLTYUf'), port=22223)

db = client["SC"]

sc = db["Sourcecode"]


def get_addr_code(transactions):
    contractaddr = set()
    transactionlist = re.findall("\('(.*?)'\)", str(transactions))
    for i in transactionlist:
        content = w3.eth.getTransaction(i)
        try:
            fromaddr = re.search("'from': '(.*?)'", str(content))[1]
            toaddr = re.search("'to': '(.*?)'", str(content))[1]
            if w3.eth.getCode(toaddr)[0:3] != b'' and toaddr not in address_set:
                contractaddr.add(toaddr)
                address_set.add(toaddr)
            if w3.eth.getCode(fromaddr)[0:3] != b'' and fromaddr not in address_set:
                contractaddr.add(fromaddr)
                address_set.add(toaddr)
        except Exception as e:
            print(e)

    for addr in contractaddr:
        api = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address=%s&apikey=%s' % (
        addr, ApiKeyToken)
        try:
            res = requests.get(api, timeout=5)
            if eval(res.text)['result'][0]['SourceCode']:
                mongodbexec(addr, eval(res.text)['result'][0]['SourceCode'])
                # with open('contract_code.txt', 'a') as f:
                #     f.write(addr + ':\r\n' + eval(res.text)['result'][0]['SourceCode'] + '\r\n\r\n')
        except Exception as e:
            print(e)


def spider(processLock, blocklist):
    transactions = []
    # threadLock.acquire()
    processLock.acquire()
    for i in range(int(len(range(blockstart, blockend)) / slice_len)):
        # threadLock.acquire()
        # processLock.acquire()
        for block in blocklist[0:slice_len]:
            print('[-] Now at block: ', block)
            try:
                transactions += (w3.eth.getBlock(block)['transactions'])
            except Exception as e:
                print(e)
        get_addr_code(transactions)
        del blocklist[0:slice_len]
        transactions = []
        # processLock.release()
        # threadLock.release()
    # threadLock.release()
    processLock.release()
    for block in blocklist:  # go over the last slice of the blocklist
        try:
            transactions += (w3.eth.getBlock(block)['transactions'])
        except Exception as e:
            print(e)
    get_addr_code(transactions)


def multi_thread_scrape(blocklist, thread):

    jobs = []
    for i in range(thread):
        # p = threading.Thread(target=spider, args=(blocklist, ))
        p = Process(target=spider, args=(processLock, blocklist, ))
        jobs.append(p)
        p.start()

    # join threads
    for job in jobs:
        if job.is_alive():
            job.join()


def mongodbexec(address, code):
    getcode = {
        'Address': address,
        'Sourcecode': code
    }
    sc.insert_one(getcode)


def send_email():
    sender = '764610677@qq.com'
    receivers = '764610677@qq.com'
    message = MIMEMultipart('related')
    subject = 'Scrape process finished!'
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receivers

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, "111")
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


def main():
    manager = Manager()
    blocklist = manager.list(range(blockstart, blockend))
    # blocklist = list(range(blockstart, blockend))
    multi_thread_scrape(blocklist=blocklist, thread=20)
    send_email()
    print('OK')


if __name__ == '__main__':
    main()
