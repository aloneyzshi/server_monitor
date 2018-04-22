#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *

from models import Host, Idc, HostGroup


class IdcForm(forms.ModelForm):
    class Meta:
        model = Idc
        fields = (
            'code', 'name', 'address', 'tel', 'contact', 'contact_phone', 'jigui', 'ip_range', 'bandwidth', 'memo')
        attributes = {'class': 'form-control', 'style': 'width:450px;'}
        widgets = {
        }
        for field in fields:
            widgets[field] = TextInput(attrs=attributes)


class HostGroupForm(forms.ModelForm):
    class Meta:
        model = HostGroup
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'desc': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:450px;'}),

        }


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'other_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_no': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'status': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'up_time': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'project':Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'position': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'物理机写位置，虚机写宿主'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }
