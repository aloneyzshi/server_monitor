# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from monitor import models


# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_addr', 'status','hostgroup')
    list_display_links = ('id', 'name')

class HostInline(admin.StackedInline):
    model = models.Host

class HostGroupAdmin(admin.ModelAdmin):
    inlines = [HostInline,]
    filter_horizontal = ('templates',)


class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('services', 'triggers',)


class ServiceIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'data_type', 'service', 'memo')
    # list_select_related = ('items',)


class ServiceIndexInline(admin.StackedInline):
    model = models.ServiceIndex


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceIndexInline, ]
    list_display = ('name', 'interval', 'plugin_name')


class TriggerExpressionInline(admin.TabularInline):
    model = models.TriggerExpression
    # exclude = ('memo',)
    # readonly_fields = ['create_date']


class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'enabled')
    inlines = [TriggerExpressionInline, ]
    # filter_horizontal = ('expressions',)


class TriggerExpressionAdmin(admin.ModelAdmin):
    list_display = (
        'trigger', 'service', 'service_index', 'specified_index_key', 'operator_type', 'data_calc_func', 'threshold',
        'logic_type')


admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup,HostGroupAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceIndex, ServiceIndexAdmin)
admin.site.register(models.Trigger, TriggerAdmin)
admin.site.register(models.TriggerExpression, TriggerExpressionAdmin)
admin.site.register(models.Action)
admin.site.register(models.ActionOperation)
admin.site.register(models.Maintenance)
admin.site.register(models.EventLog)

admin.site.site_header = '监控系统后台管理'
admin.site.site_title = '监控平台'
