#coding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from pymodel.models import AuthUser


class UserForm(forms.ModelForm):
    realname = forms.CharField(max_length=20, required=False)
    # idcart = forms.CharField(max_length=20, required=False)

    # social_city = forms.CharField(max_length=20, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']

        print(user.__dict__)

        kwargs['initial'] = {
            'realname': user.appuserprofile.realname,
            # 'idcart': user.profile.idcart
        }

        super(UserForm, self).__init__(**kwargs)

    class Meta:
        model = AuthUser
        exclude = ('',)


class PySharpUserCreationForm(UserCreationForm):
    realname = forms.CharField(label='姓名', max_length=20, required=False)
    provice = forms.CharField(label='省', max_length=10, required=False)
    city = forms.CharField(label='市', max_length=10, required=False)
    district = forms.CharField(label='区', max_length=10, required=False)
    address = forms.CharField(label='地址', max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        super(PySharpUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True  # 为了让此字段在admin中为必选项，自定义一个form


class PySharpUserChangeForm(UserChangeForm):
    realname = forms.CharField(label='姓名', max_length=20, required=False)
    provice = forms.CharField(label='省', max_length=10, required=False)
    city = forms.CharField(label='市', max_length=10, required=False)
    district = forms.CharField(label='区', max_length=10, required=False)
    address = forms.CharField(label='地址', max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']

        profile=user.appuserprofile

        kwargs['initial'] = {
            'realname': profile.realname,
            'provice': profile.provice,
            'city': profile.city,
            'district': profile.district,
            'address': profile.address
        }
        super(PySharpUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True