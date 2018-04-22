from pymongo import MongoClient
import time


class DataCaclulator:
    def __init__(self, oper, data):
        self.oper = oper
        self.data = data

    def get_res(self):
        try:
            func = getattr(self, self.oper)
        except AttributeError, e:
            message = ' func not exists'
            print message
        return func(self.data)

    def get_avg(self, data):
        return float(sum(data) / len(data))

    def get_max(self, data):
        return max(data)

    def get_min(self, data):
        return min(data)


class HostDataFetcher:

    def __init__(self, hostname, service, service_index, timing):
        self.hostname = hostname
        self.service = service
        self.service_index = service_index
        self.timing = timing

    @classmethod
    def connect_db(cls):
        mongodb_ip = '127.0.0.1'
        mongodb_port = 27017
        client = MongoClient(mongodb_ip, int(mongodb_port))
        return client

    def get_data(self):
        client = self.connect_db()
        db = client['test_monitor']
        collection = db[self.hostname]
        now_time = int(time.time())
        #now_time = 1524237771
        find_time = now_time - self.timing
        cursor = collection.find({'time': {'$gte': find_time}}, {'_id': 0})
        items = []
        for doc in cursor:
            #print doc
            #print doc['data'][self.service][self.service_index]
            items.append(doc['data'][self.service][self.service_index])

        return items


def test_main():

    #data = HostDataFetcher('mymachine', 'linux_cpu', 'idle', 1).get_data()
    data = HostDataFetcher('web_school_1', 'linux_cpu', 'idle', 5000).get_data()
    print
    funcstr = 'avg'
    res = DataCaclulator('get_%s'%(funcstr), data).get_res()
    print res

if __name__ == "__main__":
    test_main()
