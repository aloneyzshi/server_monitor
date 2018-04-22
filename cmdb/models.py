# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#from accounts.models import UserInfo


# Create your models here.
ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),

)

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"网络设备"),
    (str(5), u"安全设备"),
    (str(6), u"其他")
    )

class Idc(models.Model):

    code = models.CharField(u'机房代号',max_length=255,unique=True)
    name = models.CharField(u"机房名称", max_length=255, unique=True)
    address = models.CharField(u"机房地址", max_length=100, blank=True)
    tel = models.CharField(u"机房电话", max_length=30, blank=True)
    contact = models.CharField(u"客户经理", max_length=30, blank=True)
    contact_phone = models.CharField(u"联系电话", max_length=30, blank=True)
    jigui = models.CharField(u"机柜信息", max_length=30, blank=True)
    ip_range = models.CharField(u"IP范围", max_length=30, blank=True)
    bandwidth = models.CharField(u"接入带宽", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = verbose_name



class HostGroup(models.Model):
    name = models.CharField(u"项目名", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, null=True, blank=True)
    #members = models.ManyToManyField(UserInfo,verbose_name=u'组内成员')

    class Meta:
        verbose_name = u'主机组'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    ip = models.GenericIPAddressField(u"管理IP", max_length=15)
    other_ip = models.CharField(u"其它IP", max_length=100, null=True, blank=True)
    project = models.ForeignKey(HostGroup, verbose_name=u"设备组", on_delete=models.SET_NULL, null=True, blank=True)
    asset_no = models.CharField(u"资产编号", max_length=50, null=True, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, null=True, blank=True)
    vendor = models.CharField(u"设备厂商", max_length=50, null=True, blank=True)
    up_time = models.CharField(u"上架时间", max_length=50, null=True, blank=True)
    cpu_model = models.CharField(u"CPU型号", max_length=100, null=True, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, null=True, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, null=True, blank=True)
    disk = models.CharField(u"硬盘信息", max_length=255, null=True, blank=True)
    sn = models.CharField(u"SN号码", max_length=60, blank=True)
    position = models.CharField(u"所在位置", max_length=100, null=True, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, null=True, blank=True)
    idc = models.ForeignKey(Idc, verbose_name=u"所在机房", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.hostname


