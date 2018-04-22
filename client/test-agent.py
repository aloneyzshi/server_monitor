import os
import schedule
import threading
import datetime
import time


def run_plugin(pluginname,interval):
    try:

        plugin = __import__("plugins." + pluginname, fromlist=[pluginname])
    except ValueError, e:
        message = 'import key#%s val#%s with error %s' % (pluginname, e)
        print message

    try:
        plugin_func = getattr(plugin, pluginname)
    except AttributeError, e:
        message = 'plugin key#%s val#%s not exists' % (plugin, pluginname)

    return plugin_func,interval


def plugin_1(id):
    print id
    print "plugin_1: ", datetime.datetime.now()


def plugin_2():
    print "plugin_2: ", datetime.datetime.now()


def task1():
    threading.Thread(target=plugin_1, args=(1)).start()


def task2():
    threading.Thread(target=plugin_2).start()


def start(task):
    print task
    threading.Thread(target=task).start()


def test_main_run(s,plugname):
    schedule.every(s).seconds.do(start, plugname)


func,interval = run_plugin('get_windows_cpu',3)
test_main_run(interval,func)

while True:
   schedule.run_pending()




'''
1 load_config
2 invoke_plugins
    
    test_main_run(plugfunc,interval)
        schedule.every(s).seconds.do(start, plugfuncname)

3 post every_plugin_data
'''
