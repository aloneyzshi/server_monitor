#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from models import ASSET_STATUS, ASSET_TYPE, Host
from forms import HostForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def asset_list(request):
    temp_name = "cmdb/cmdb-header.html"

    all_asset = Host.objects.all()
    return render(request, 'cmdb/asset_list.html', locals())


@login_required()
@permission_verify()
def asset_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = HostForm()
    return render(request, 'cmdb/asset_add.html', locals())


@login_required()
@permission_verify()
def asset_edit(request, id):
    status = 0
    asset_types = ASSET_TYPE
    host = Host.objects.get(id=id)

    if request.method == 'POST':
        form = HostForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = HostForm(instance=host)
    return render(request, 'cmdb/asset_edit.html', locals())


@login_required()
@permission_verify()
def asset_del(request):
    asset_id = request.GET.get('id', '')

    if asset_id:
        print asset_id
        # Host.objects.filter(id=asset_id).delete()

    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))
        asset_ids = request.POST.getlist('asset_check', [])
        if asset_batch:
            for asset_id in asset_id_all.split(','):
                Host.objects.filter(id=asset_id).delete()

    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def asset_detail(request, id):
    host = Host.objects.get(id=id)
    return render(request, 'cmdb/host_detail.html', locals())
