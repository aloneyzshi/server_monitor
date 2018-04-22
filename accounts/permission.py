# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import Permission, UserInfo, Role
from forms import ListPermissionForm
from django.contrib.auth.decorators import login_required


def permission_verify():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = UserInfo.objects.get(username=request.user.username)

            if not user.is_superuser:
                rolelist = user.role.select_related()
                if not rolelist:
                    return redirect(('permission_deny'))

                elif rolelist:
                    for role in rolelist:
                        print role
                        print dir(role)
                        role = Role.objects.get(name=role.name)

                        permission_list = role.permission.select_related()
                        print permission_list

                    matchurl = []

                    for perm in permission_list:
                        print perm.allowed_url
                        print request.path

                        if request.path == perm.allowed_url or request.path.rstrip('/') == perm.allowed_url:
                            matchurl.append(perm.allowed_url)
                        elif request.path.startswith(perm.allowed_url):
                            matchurl.append(perm.allowed_url)
                        else:
                            pass

                    print('{}---->matchUrl:{}'.format(request.user, str(matchurl)))

                    if len(matchurl) == 0:
                        return redirect(('permission_deny'))

                else:
                    pass

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@login_required()
def permission_deny(request):
    temp_name = "main-header.html"
    roles = UserInfo.objects.get(username=request.user.username)

    print roles
    return render(request, 'accounts/permission_deny.html', locals())


@login_required()
@permission_verify()
def permission_list(request):
    all_permission = Permission.objects.all()
    temp_name = "accounts/accounts-header.html"
    return render(request, 'accounts/permission_list.html', locals())


@login_required()
@permission_verify()
def permission_add(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = ListPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(('permission_list'))
    else:
        form = ListPermissionForm()
    return render(request, 'accounts/permission_add.html', locals())


@login_required()
@permission_verify()
def permission_edit(request, id):
    temp_name = "accounts/accounts-header.html"
    permission = Permission.objects.get(id=id)
    if request.method == 'POST':
        form = ListPermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
            return redirect(('permission_list'))
    else:
        form = ListPermissionForm(instance=permission)
    return render(request, 'accounts/permission_edit.html', locals())


@login_required()
@permission_verify()
def permission_del(request, id):
    if id:
        Permission.objects.filter(id=id).delete()
    return redirect(('permission_list'))
