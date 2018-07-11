from pyquery import PyQuery as pq
import pymongo
import requests


# url = 'https://etherscan.io/tx/0x51d0643db9a5c7ddf87388e7f1f5aaef13056f3dd5152691ee1ef778a1e2e1ae'
# r = requests.get(url)
# text = r.text
#
# doc = pq(url='https://etherscan.io/txs')
#
# tr = doc('tr')
#
# print(tr('.address-tag')('a'))

# for tr in tr.items():
#     data = tr('td').eq(2).text()

client = pymongo.MongoClient("mongodb://%s:%s@127.0.0.1" % ('root', 'password'), port=22222)

db = client["SC"]

sc = db["transactions"]


def mongodbexec(From, To):
    transaction = {
        'from': From,
        'to': To
    }
    sc.insert_one(transaction)


# txurl = 'https://etherscan.io/tx/0x12320bed61ba1784f43e4ba345a4c27551f4f2776336a26fac6c512b11373df6'
# txurl = 'https://etherscan.io/tx/0x541ba63c21137087134fdf654165e06160fdfab085401124b82d6929c241f7b4'
# txurl = 'https://etherscan.io/tx/0x6507723918d7bd89dad2bba09f50784fcaee5659eb8c9f0181c0af74cd5b9d08'
txurl = 'https://etherscan.io/tx/0x49fcd2b80e2ec394fe350de7b32e8a8a929f808adecf55899211339ff940a4ed'

doc = pq(url=txurl)

div = doc('div')

From, To = div('.col-sm-9').eq(4).text(), div('.col-sm-9').eq(5).text()

if 'contract' in From or To:
    try:
        mongodbexec(From, To)
    except Exception as e:
        print(e)

# print('from %s to %s' % (From, To))

# print(div('.col-sm-9').eq(5).text())

# print(div('.panel-body').eq(0).text())

# print(div('.col-sm-9 cbs'))



