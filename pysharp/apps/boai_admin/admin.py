#coding:utf-8

from django.contrib import admin

from pysharp.apps.boai_admin.models import AppCompany


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppCompany,CompanyAdmin)