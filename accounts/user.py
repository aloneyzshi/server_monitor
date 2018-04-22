# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from forms import LoginForm, AddUserForm, EditUserForm, ChangePwdForm
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify


# Create your views here.


def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # next_page = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        if next == "/accounts/logout/":
            next = '/'
        form = LoginForm(request)
        return render(request, 'accounts/login.html', locals())

    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
        else:
            return render(request, 'accounts/login.html', locals())
    else:

        return render(request, 'accounts/login.html', locals())

@login_required()
def logout(request):
    auth.logout(request)
    return redirect('login')


def index(request):
    return HttpResponse('accounts  index page ')

@login_required()
@permission_verify()
def user_list(request):
    temp_name = "accounts/accounts-header.html"
    all_user = auth.get_user_model().objects.all()

    return render(request, 'accounts/user_list.html', locals())


@login_required()
@permission_verify()
def user_add(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        print dir(form)
        print form.errors
        if form.is_valid():
            print form.errors
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return redirect(('user_list'))

    else:
        form = AddUserForm()

    args = {
        'form':form,
        'request':request,
        'temp_name':temp_name
    }
    return render(request, 'accounts/user_add.html', args)



@login_required()
@permission_verify()
def user_del(request,id):
    if id:
        auth.get_user_model().objects.filter(id=id).delete()

    return HttpResponseRedirect(('user_list'))


@login_required()
@permission_verify()
def user_edit(request,id):
    temp_name = "accounts/accounts-header.html"
    user = auth.get_user_model().objects.get(id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'accounts/user_edit.html', locals())


@login_required()
@permission_verify()
def reset_password(request,id):

    user = auth.get_user_model().objects.get(id=id)
    newpassword = auth.get_user_model().objects.make_random_password(length=12,allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY123456789~!@#$%^&')
    user.set_password(newpassword)
    user.save()

    return HttpResponse('账户 %s 的密码已重置为 <font style="font-size:16px;color: red;font-weight: bold;"> %s </font>' % (user.username,newpassword))


@login_required()
def change_password(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = ChangePwdForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logout'))
    else:
        form = ChangePwdForm(request.user)
    kwargs = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'accounts/change_password.html', kwargs)

