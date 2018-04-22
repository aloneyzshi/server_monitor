# -*- coding: utf-8 -*-


from django.shortcuts import render, HttpResponse, redirect
from models import Role, Permission
from forms import ListRoleForm
from accounts.permission import permission_verify
from django.contrib.auth.decorators import login_required


@login_required()
@permission_verify()
def role_list(request):
    temp_name = "accounts/accounts-header.html"
    all_role = Role.objects.all()
    return render(request, 'accounts/role_list.html', locals())


@login_required()
@permission_verify()
def role_add(request):
    temp_name = "accounts/accounts-header.html"

    if request.method == 'POST':

        form = ListRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(('role_list'))

    else:
        form = ListRoleForm()

    return render(request, 'accounts/role_add.html', locals())


@login_required()
@permission_verify()
def role_edit(request, id):
    temp_name = "accounts/accounts-header.html"
    role = Role.objects.get(id=id)

    if request.method == 'POST':
        form = ListRoleForm(request.POST,instance=role)
        if form.is_valid():
            form.save()
            return redirect(('role_list'))

    else:
        form = ListRoleForm(instance=role)

    return render(request, 'accounts/role_edit.html', locals())


@login_required()
@permission_verify()
def role_del(request, id):

    return HttpResponse(id)
