# -*- coding: utf-8 -*-
import requests
import json
import settings
import schedule
import threading
import datetime
import time
import random


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


class Agent:

    def __init__(self):
        self.agent_init_conf = settings.config
        self.id = self.agent_init_conf['client_id']
        self.agent_gather_conf = dict()
        self.config_url = self.agent_init_conf['config_url']

    def post_data(self, url, data):
        requests.post(url, data=data)

    def load_lastest_config(self):
        config = json.loads(requests.get(self.config_url + str(self.id)).content)
        self.agent_gather_conf = config
        print config

    def load_plugin(self, service_name, pluginname):
        try:
            pluginmod = __import__("plugins." + pluginname, fromlist=[pluginname])
        except ValueError, e:
            message = 'import key#%s val#%s with error %s' % (pluginname, e)
            print message

        try:
            plugin_func = getattr(pluginmod, pluginname)
            return service_name, plugin_func

        except AttributeError, e:
            message = 'plugin key#%s val#%s not exists' % (pluginmod, pluginname)
            print message
            return None

    def start(self, task):

        pluginthread = MyThread(task)
        pluginthread.start()
        pluginthread.join()
        print " %s : %s " % (datetime.datetime.now(), task.__name__)
        if pluginthread.get_result() is not None:
            print pluginthread.get_result()

        '''
                pluginthread = threading.Thread(target=task)
                pluginthread.start()
                pluginthread.join()

        '''

    def run_plugin(self, plugname, interval):
        '''
        run and post data to server
        :return:
        '''

        schedule.every(interval).seconds.do(self.start, plugname)


def main():
    agent = Agent()
    # agent.load_lastest_config(agent.agent_init_conf['config_url'], agent.agent_init_conf['client_id'])
    agent.load_lastest_config()

    for service in agent.agent_gather_conf['service'].keys():
        pluginname = agent.agent_gather_conf['service'][service][0]
        interval = agent.agent_gather_conf['service'][service][1]
        service_name, plugin_func = agent.load_plugin(service, pluginname)
        agent.run_plugin(plugin_func, interval)

    agent.run_plugin(agent.load_lastest_config, 30)

    while True:
        schedule.run_pending()


def test_post(url, data):
    try:
        r = requests.post(url, data=data)
        print r.content
        return r.status_code
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print e
        return True


def gendata(t):
    idle = round(random.uniform(0, 100), 2)
    system = round((random.uniform(0, int(idle))), 2)
    user = round(100 - system, 2)
    cpu_percent = round(100 - idle, 2)

    total = 8103L
    used = long(random.uniform(2000, 5000))
    available = total - used
    free = available
    men_percent = round(round(used,2) / total*100,1)

    info = {'hostname': 'web_school_1',
            # 'time': time.strftime("%Y%m%d-%H:%M:%S", time.localtime(t)),
            'time': t,
            'data': {'linux_cpu': {'idle': idle,
                                   'system': system,
                                   'percent': cpu_percent,
                                   'user': user},
                     'linux_mem': {'available': available,
                                   'total': total,
                                   'percent': men_percent,
                                   'free': free,
                                   'used': used}
                     }
            }


    return info


def genetate():
    for t in range(int(time.time() - 180), int(time.time())):
        info = gendata(t)
        url = 'http://127.0.0.1:8000/monitor/api/update/'
        test_post(url, json.dumps(info))
        print info


if __name__ == '__main__':
    # main()

     info = {u'id':1,u'hostname': u'web_school_1', u'service': {u'linux_cpu': [u'get_linux_cpu', 60], u'linux_mem': [u'get_linux_mem', 30], u'linux_net': [u'get_linux_net', 60], u'linux_disk': [u'get_linux_disk', 60]}}
     url = 'http://127.0.0.1:8000/monitor/api/update/'
     test_post(url,json.dumps(info))

    #genetate()

'''
collection:hostname

hostinfo= {
hostname:mymachine
time:20180501
data:{linux_cpu:{cpu.idle:94.2,cpu.system:3.1}
}
'''

'''


1 x 60秒 x 60分钟 x 24小时 x 365天 = 31536000


'''
