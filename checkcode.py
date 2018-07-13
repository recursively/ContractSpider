import pymongo
import subprocess
import os


class MongodbConn(object):

    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://%s:%s@192.168.10.220" % ('root', 'ATWtGZhsP4FLTYUf'), port=22223)
        self.count = 1

    def run(self):
        db = self.connection['SC']
        sc = db.Sourcecode
        cursor = sc.find()
        total = cursor.count()
        if not os.path.exists('contracts'):
            os.mkdir('contracts')
        for document in cursor:
            print(str(self.count) + '/' + str(total))
            addr = document['Address']
            sourcecode = document['Sourcecode']
            if not os.path.exists('./contracts/' + addr):
                os.mkdir('./contracts/' + addr)
            with open('./contracts/' + addr + '/' + addr + '.sol', 'w') as f:
                f.write(sourcecode)
            os.chdir('./contracts/' + addr)
            try:
                subprocess.call('manticore ' + addr + '.sol', shell=True)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    mongo_obj = MongodbConn()
    mongo_obj.run()
