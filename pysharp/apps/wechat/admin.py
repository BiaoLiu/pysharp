import json

from django.contrib import admin

# Register your models here.
from pysharp.apps.wechat import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'success', 'content', 'created_time')
    save_on_top = True
    access_token = None

    def save_model(self, request, obj, form, change):
        try:
            if self.set_menu(obj):
                obj.success = True
        except Exception as e:
            obj.response_data = str(e)
        obj.save()

    # def set_menu(self, obj):
    #     # 调用微信设置菜单接口
    #     if not self.access_token:
    #         self.get_access_token()
    #
    #     content = obj.content.encode('utf-8')
    #     f = requests.post(weixin_menu % self.access_token, data=content)
    #     data = json.loads(f.content)
    #     if data['errcode'] == 0:
    #         return True
    #     elif data['errcode'] == 42001:
    #         self.get_access_token()
    #         return self.set_menu(content)
    #     else:
    #         obj.response_data = data
    #
    # # def get_access_token(self):
    # #     content = urllib2.urlopen(get_access_token).read()
    # #     data = json.loads(content)
    # #     self.access_token = data['access_token']


@admin.register(models.ResponseMessage)
class ResponseMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'content', 'created_time')
    save_on_top = True

@admin.register(models.Message)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'to', 'from_user', 'msg_id', 'content', 'response_content', 'created_time')
    save_on_top = True

    def content(self, obj):
        data = json.loads(obj.body)
        return data['content']
    content.short_description = '内容'
    content.allow_tags = True


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'to', 'from_user', 'event', 'body', 'created_time')
    save_on_top = True

