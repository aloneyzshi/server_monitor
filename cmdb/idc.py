# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from forms import IdcForm
from models import Idc
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.permission import  permission_verify


@login_required()
@permission_verify()
def idc_list(request):
    temp_name = "cmdb/cmdb-header.html"

    all_idc = Idc.objects.all()

    return render(request, 'cmdb/idc_list.html', locals())


@login_required()
@permission_verify()
def idc_add(request):
    temp_name = "cmdb/cmdb-header.html"

    if request.method == 'POST':
        form = IdcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('idc_list')
    else:
        form = IdcForm
    return render(request, 'cmdb/idc_add.html', locals())


@login_required()
@permission_verify()
def idc_edit(request, id):
    temp_name = "cmdb/cmdb-header.html"
    idc = Idc.objects.get(id=id)

    if request.method == 'POST':
        form = IdcForm(request.POST, instance=idc)
        if form.is_valid():
            form.save()
            return redirect('idc_list')
    else:
        form = IdcForm(instance=idc)

    return render(request, 'cmdb/idc_edit.html', locals())


@login_required()
@permission_verify()
def idc_del(request):
    idc_id = request.GET.get('id', '')
    if idc_id:
        Idc.objects.filter(id=idc_id).delete()
        print idc_id
    if request.method == 'POST':
        idc_ids = request.POST.getlist('idc_check', [])
        if idc_ids:
            for id in idc_ids:
                Idc.objects.filter(id=id).delete()
    return redirect(('idc_list'))

@login_required()
@permission_verify()
def idc_detail(request,id):
    idc = Idc.objects.get(id=id)
    return render(request, 'cmdb/idc_detail.html', locals())

