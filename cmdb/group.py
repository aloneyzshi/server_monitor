#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import Host, HostGroup
from forms import HostGroupForm
from django.contrib.auth.decorators import login_required
from accounts.permission import  permission_verify

@login_required()
@permission_verify()
def group_list(request):
    temp_name = "cmdb/cmdb-header.html"
    all_group = HostGroup.objects.all()


    return render(request, 'cmdb/group_list.html', locals())


@login_required()
@permission_verify()
def group_add(request):
    temp_name = "cmdb/cmdb-header.html"

    if request.method == 'POST':
        form = HostGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = HostGroupForm()
    return render(request, 'cmdb/group_add.html', locals())


@login_required()
@permission_verify()
def group_del(request):
    temp_name = "cmdb/cmdb-header.html"

    group_id = request.GET.get('id', '')

    if group_id:
        HostGroup.objects.filter(id=group_id).delete()

    if request.method == 'POST':
        group_items = request.POST.getlist('group_check', [])
        if group_items:
            for n in group_items:
                HostGroup.objects.filter(id=n).delete()
    all_group = HostGroup.objects.all()
    return render(request, "cmdb/group_list.html", locals())


@login_required()
@permission_verify()
def group_edit(request, id):
    temp_name = "cmdb/cmdb-header.html"
    # obj = HostGroup.objects.get(id=id)
    # allgroup = HostGroup.objects.all()
    # unselect = Host.objects.filter(group__name=None)
    # members = Host.objects.filter(group__name=obj.name)

    group = HostGroup.objects.get(id=id)
    if request.method == 'POST':
        form = HostGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect(('group_list'))

    else:
        form = HostGroupForm(instance=group)
    return render(request, "cmdb/group_edit.html", locals())


@login_required()
@permission_verify()
def group_detail(request, id):
    group = HostGroup.objects.get(id=id)
    hosts = group.host_set.select_related()

    return render(request, 'cmdb/group_detail.html', locals())



