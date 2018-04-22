from pymongo import MongoClient
import time

data = {'hostname': 'web_school_1',
        'time': time.time(),
        'data': {'linux_cpu': {'idle': 94.2,
                               'system': 3.1,
                               'percent': 90,
                               'user': 3}
                 }
        }

client = MongoClient('mongodb://localhost:27017')
db = client['test_monitor']
collection = db[data['hostname']]
#rs = collection.insert_one(data)
rs  = collection.find()
print rs


#for doc in rs:
#    print doc
#    print type(doc)

doc = {u'data': {u'linux_cpu': {u'idle': 61.75, u'percent': 38.25, u'system': 41.83, u'user': 58.17}}, u'hostname': u'mymachine', u'time': 1524237771}




