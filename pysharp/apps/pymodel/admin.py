from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from pymodel import models
from pymodel.forms import PySharpUserChangeForm, PySharpUserCreationForm


class PySharpUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(PySharpUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'email', 'nickname')

        self.form = PySharpUserChangeForm  # 编辑用户表单
        self.add_form = PySharpUserCreationForm  # 添加用户表单

    def changelist_view(self, request, extra_context=None):
        # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同

        self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                          (_('Personal info'),
                           {'fields': ('realname', 'mobile', 'email', 'provice', 'city', 'district', 'address')}),
                          (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                          (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                          )
        self.add_fieldsets = ((None, {'classes': ('wide',),
                                      'fields': (
                                          'username', 'mobile', 'password1', 'password2', 'realname', 'email',
                                          'provice', 'city', 'district',
                                          'is_active',
                                          'is_staff', 'is_superuser', 'groups'),
                                      }),
                              )

        return super(PySharpUserAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        cleaned_data = form.cleaned_data
        obj.save()

        if not change:
            user_profile = models.AppUserProfile(user_id=obj.id)
        else:
            user_profile = form.instance.appuserprofile

        user_profile.realname = cleaned_data.get('realname')
        user_profile.provice = cleaned_data.get('provice')
        user_profile.city = cleaned_data.get('city')
        user_profile.district = cleaned_data.get('district')
        user_profile.address = cleaned_data.get('address')
        user_profile.save()


admin.site.register(models.AuthUser, PySharpUserAdmin)
