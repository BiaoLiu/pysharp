from django.contrib import admin
import xadmin

# Register your models here.
from boai.models import AppCompany


class AppCompanyAdmin:
    pass


xadmin.sites.site.register(AppCompany,AppCompanyAdmin)