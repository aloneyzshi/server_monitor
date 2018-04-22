#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from cmdb import asset, idc, group

urlpatterns = [
    # url(r'asset/$', asset.asset, name='cmdb'),
    url(r'^asset/list/$', asset.asset_list, name='asset_list'),
    url(r'^asset/add/$', asset.asset_add, name='asset_add'),
    url(r'^asset/delete/$', asset.asset_del, name='asset_del'),

    url(r'^asset/edit/(?P<id>\d+)/$', asset.asset_edit, name='asset_edit'),
    url(r'^asset/detail/(?P<id>\d+)/$', asset.asset_detail, name='asset_detail'),

    url(r'^idc/list/$', idc.idc_list, name='idc_list'),
    url(r'^idc/add/$', idc.idc_add, name='idc_add'),
    url(r'^idc/edit/(?P<id>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^idc/delete/$', idc.idc_del, name='idc_del'),
    url(r'^idc/detail/(?P<id>\d+)/$', idc.idc_detail, name='idc_detail'),

    url(r'^group/list/$', group.group_list, name='group_list'),
    url(r'^group/add/$', group.group_add, name='group_add'),
    url(r'^group/delete/$', group.group_del, name='group_del'),
    url(r'^group/edit/(?P<id>\d+)/$', group.group_edit, name='group_edit'),
    url(r'^group/detail/(?P<id>\d+)/$', group.group_detail, name='group_detail'),

]
