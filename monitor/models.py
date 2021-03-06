# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# from cmdb.models import Host
from django.contrib import auth
from django.db import models


# Create your models here.

class HostGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    templates = models.ManyToManyField("Template", blank=True)
    memo = models.TextField(u"备注", blank=True, null=True)

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


'''
falcon无需配置，只要agent部署到机器上，配置好heartbeat和Transfer地址，
就自动开始采集了，省去了用户配置的麻烦。

基础监控是指只要是个机器(或容器)就能加的监控，比如cpu mem net io disk等，
这些监控采集的方式固定，不需要配置，也不需要用户提供额外参数指定，只要agent跑起来就可以直接采集上报上去； 
非基础监控则相反，比如端口监控，你不给我端口号就不行，不然我上报所有65535个端口的监听状态你也用不了，
这类监控需要用户配置后才会开始采集上报的监控（包括类似于端口监控的配置触发类监控，
以及类似于mysql的插件脚本类监控），一般就不算基础监控的范畴了。

'''


class Host(models.Model):
    name = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    hostgroup = models.ForeignKey("HostGroup", blank=True)
    monitored_by_choices = (
        ('agent', 'Agent'),
        ('snmp', 'SNMP'),
        ('wget', 'WGET'),
    )
    monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
    status_choices = (
        (1, 'Online'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Offline'),
        (5, 'Problem'),
    )
    host_alive_check_interval = models.IntegerField(u"主机存活状态检测间隔", default=30)
    status = models.IntegerField(u'状态', choices=status_choices, default=1)
    memo = models.TextField(u"备注", blank=True, null=True)

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s : %s " % (self.name, self.ip_addr)


class ServiceIndex(models.Model):
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64)
    data_type_choices = (
        ('int', "int"),
        ('float', "float"),
        ('str', "string")
    )
    data_type = models.CharField(u'指标数据类型', max_length=32, choices=data_type_choices, default='int')
    memo = models.CharField(u"备注", max_length=128, blank=True, null=True)
    service = models.ForeignKey("Service", verbose_name=u"所属服务")

    class Meta:
        verbose_name = u'服务指标'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(u'服务名称', max_length=64, unique=True)
    interval = models.IntegerField(u'监控间隔', default=60)
    plugin_name = models.CharField(u'插件名', max_length=64, default='n/a')
    # items = models.ManyToManyField('ServiceIndex', verbose_name=u"指标列表", blank=True)
    # items = models.ForeignKey('ServiceIndex',verbose_name=u"指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,
                                          help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡")  # 如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    memo = models.CharField(u"备注", max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = u'服务'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Template(models.Model):
    name = models.CharField(u'模版名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service', verbose_name=u"服务列表")
    triggers = models.ManyToManyField('Trigger', verbose_name=u"触发器列表", blank=True)

    class Meta:
        verbose_name = u'监控模版'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class TriggerExpression(models.Model):
    trigger = models.ForeignKey('Trigger', verbose_name=u"所属触发器")
    service = models.ForeignKey(Service, verbose_name=u"关联服务")
    service_index = models.ForeignKey(ServiceIndex, verbose_name=u"关联服务指标")
    specified_index_key = models.CharField(verbose_name=u"只监控专门指定的指标key", max_length=64, blank=True, null=True)
    operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
    operator_type = models.CharField(u"运算符", choices=operator_type_choices, max_length=32)
    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'),
    )
    data_calc_func = models.CharField(u"数据处理方式", choices=data_calc_type_choices, max_length=64)
    data_calc_args = models.CharField(u"函数传入参数", help_text=u"若是多个参数,则用,号分开,第一个值是时间", max_length=64)
    threshold = models.IntegerField(u"阈值")
    logic_type_choices = (('or', 'OR'), ('and', 'AND'))
    logic_type = models.CharField(u"与一个条件的逻辑关系", choices=logic_type_choices, max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'触发条件'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s (%s(%s)) %s %s" % (
        self.service_index, self.data_calc_func, self.data_calc_args, self.operator_type, self.threshold)


class Trigger(models.Model):
    name = models.CharField(u'触发器名称', max_length=64)
    severity_choices = (
        (1, 'Information'),
        (2, 'Warning'),
        (3, 'Average'),
        (4, 'High'),
        (5, 'Diaster'),
    )
    # expressions = models.ManyToManyField(TriggerExpression,verbose_name=u"条件表达式")
    severity = models.IntegerField(u'告警级别', choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(u"备注", blank=True, null=True)

    class Meta:
        verbose_name = u'触发器'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "<service:%s, severity:%s>" % (self.name, self.get_severity_display())


class Action(models.Model):
    """定义trigger发生后，如何报警"""
    name = models.CharField(max_length=64, unique=True)  # 磁盘将满动作 rootdiskusedactions
    # host_groups = models.ManyToManyField('HostGroup', blank=True)  # 在template里已经关联了主机和tirgger了，为什么这里还要有
    # hosts = models.ManyToManyField('Host', blank=True)
    triggers = models.ManyToManyField('Trigger', blank=True, help_text=u"想让哪些trigger触发当前报警动作")

    interval = models.IntegerField(u'告警间隔(s)', default=300)
    operations = models.ManyToManyField('ActionOperation')

    recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
    recover_subject = models.CharField(max_length=128, blank=True, null=True)
    recover_message = models.TextField(blank=True, null=True)

    enabled = models.BooleanField(default=True)

    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''

    msg_format = models.TextField(u"消息格式", default=_msg_format)

    class Meta:
        verbose_name = u'报警'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class ActionOperation(models.Model):
    """报警操作列表"""
    name = models.CharField(max_length=64)
    step = models.SmallIntegerField(u"第n次告警", default=1, help_text="当trigger触发次数小于这个值时就执行这条记录里报警方式")
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(u"操作类型", choices=action_type_choices, default='email', max_length=64)
    notifiers = models.ManyToManyField(auth.get_user_model(), verbose_name=u"通知对象", blank=True)

    # _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''

    # msg_format = models.TextField(u"消息格式", default=_msg_format)

    class Meta:
        verbose_name = u'报警操作'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Maintenance(models.Model):
    name = models.CharField(max_length=64, unique=True)
    host = models.ManyToManyField('Host', blank=True)
    hostgroup = models.ManyToManyField('HostGroup', blank=True)
    content = models.TextField(u"维护内容")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = u'维护操作'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class EventLog(models.Model):
    """存储报警及其它事件日志"""
    event_type_choices = ((0, '报警事件'), (1, '维护事件'))
    event_type = models.SmallIntegerField(choices=event_type_choices, default=0)
    host = models.ForeignKey("Host")
    trigger = models.ForeignKey("Trigger", blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'报警记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "host%s  %s" % (self.host, self.log)
