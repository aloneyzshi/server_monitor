# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Host, HostGroup, Idc

# Register your models here.





class HostAdmin(admin.ModelAdmin):
    list_display = ['hostname','ip','project','vendor','os','cpu_model','cpu_num','sn']



class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name','desc']
    search_fields = ['name']

    #filter_horizontal = ('members',)

class IdcAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'address',
                    ]


admin.site.register(Host,HostAdmin)
admin.site.register(HostGroup,HostGroupAdmin)
admin.site.register(Idc,IdcAdmin)


