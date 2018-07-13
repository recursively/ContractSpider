import pymongo
import subprocess
import os


class MongodbConn(object):

    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://%s:%s@192.168.10.220" % ('root', 'ATWtGZhsP4FLTYUf'), port=22223)

    def run(self):
        db = self.connection['SC']
        sc = db.Sourcecode
        cursor = sc.find()
        if not os.path.exists('contracts'):
            os.mkdir('contracts')
        for document in cursor:
            addr = document['Address']
            sourcecode = document['Sourcecode']
            if not os.path.exists('./contracts/' + addr):
                os.mkdir('./contracts/' + addr)
            with open('./contracts/' + addr + '/' + addr + '.sol', 'w') as f:
                f.write(sourcecode)
            # files = subprocess.Popen('ls', shell=True)
            # subprocess.call('manticore ' + '-h', shell=True)


if __name__ == '__main__':
    mongo_obj = MongodbConn()
    mongo_obj.run()
