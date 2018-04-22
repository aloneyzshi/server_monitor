# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from monitor import models
import json
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from backends import data_process


# Create your views here.


def index(request):
    temp_name = 'monitor/monitor-header.html'
    all_asset = models.Host.objects.all()
    return render(request, 'monitor/asset_list.html', locals())


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        client = MongoClient('mongodb://localhost:27017')
        db = client['test_monitor']
        collection = db[info['hostname']]
        rs = collection.insert_one(info)
        print rs.inserted_id
    return HttpResponse("post success")


def judge(hostname, condition):
    print "judge------------------------"
    print hostname
    print condition
    # print condition.service_index.service.name
    # print condition.service_index.key
    data = data_process.HostDataFetcher(hostname, condition.service_index.service.name, condition.service_index.key,
                                        505500).get_data()
    # 记得把第三个参数 timing 改为 condition.data_calc_args

    res = data_process.DataCaclulator('get_%s' % (condition.data_calc_func), data).get_res()
    print res
    if condition.operator_type == 'lt':
        return (True, res) if res < condition.threshold else (False, res)
    if condition.operator_type == 'gt':
        return (True, res) if res > condition.threshold else (False, res)
    if condition.operator_type == 'eq':
        return (True, res) if res == condition.threshold else (False, res)


@csrf_exempt
def test_receive(request):
    info = json.loads(request.body)
    host = models.Host.objects.get(id=info['id'])
    print host.name
    hostgroup = host.hostgroup
    print hostgroup
    templates = hostgroup.templates
    # print templates.select_related()  # <QuerySet [<Template: system-basic>, <Template: system-io>]>

    # print templates.values() #<QuerySet [{u'id': 1, 'name': u'system-basic'}, {u'id': 2, 'name': u'system-io'}]>

    for template in templates.select_related():
        print template.services.select_related()

        for trigger in template.triggers.select_related():
            print trigger
            print trigger.enabled
            print trigger.severity

            conditions = trigger.triggerexpression_set.select_related().order_by('id')

            judegresults = []
            for condition in conditions:
                print condition  # condition.logic_type
                # print condition.service_index.service.name, condition.service_index
                judegres = judge(host.name, condition)
                judegresults.append(judegres)

                # if condition.logic_type == 'and':
                # elif condition.logic_type == '':
                #    judegresults.append(judegres)
                # elif condition.logic_type == 'or':

            print judegresults
        return HttpResponse("judge success")

        # for trigger in template.triggers.select_related():
    #    print trigger.triggerexpression_set.select_related()

    return HttpResponse("test_receive_success")


@csrf_exempt
def hostinfo(request, id):
    return render(request, 'monitor/test-charts.html', locals())


def get_data(request, id):
    client = MongoClient('mongodb://localhost:27017')
    db = client['test_monitor']
    collection = db['web_school_1']
    rs = collection.find()
    timelist = []
    data_idle_list = []
    data_percent_list = []
    data_system_list = []
    data_user_list = []
    for doc in rs:
        # timelist.append(time.strftime("%Y%m%d-%H:%M:%S", time.localtime(doc['time'])))
        timelist.append(doc['time'])
        data_idle_list.append(doc['data']['linux_cpu']['idle'])
        data_percent_list.append(doc['data']['linux_cpu']['percent'])
        data_system_list.append(doc['data']['linux_cpu']['system'])
        data_user_list.append(doc['data']['linux_cpu']['user'])
    return render(request, 'monitor/test-charts.html', locals())
    # return HttpResponse(rs)


@csrf_exempt
def send_config(request, id):
    config = {'service': {}}
    host = models.Host.objects.get(id=id)
    hostgroup = host.hostgroup
    print hostgroup
    print dir(hostgroup)
    print hostgroup.host_set.all()
    templates = hostgroup.templates
    print '*' * 25
    print dir(templates)
    print '*' * 25
    print templates.select_related()  # <QuerySet [<Template: system-basic>, <Template: system-io>]>

    # print templates.values() #<QuerySet [{u'id': 1, 'name': u'system-basic'}, {u'id': 2, 'name': u'system-io'}]>

    for template in templates.select_related():
        print template.services.select_related()
        for service in template.services.select_related():
            print service.name
            # print dir(service)
            # print service.serviceindex_set.all()
            # <QuerySet [<ServiceIndex: linux_net.traffic_in.traffic_in>, <ServiceIndex: linux_net.traffic_out.traffic_out>]>
            print '-' * 25

            config['service'][service.name] = [service.plugin_name, service.interval]

    print config

    # templates_list = models.Host.objects.get(id=id).hostgroup.templates.select_related()
    # print templates_list

    if config:
        config['hostname'] = host.name
        return HttpResponse(json.dumps(config))

    return HttpResponse(id)
