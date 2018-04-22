#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse, redirect


def index(request):
    return redirect('user_list')