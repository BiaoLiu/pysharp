from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.AppQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'user', 'abstract','question_mode','question_price','status','createtime']
    exclude = ['question_id']

    def abstract(self, instance):
        return instance.content[0:20]

    abstract.short_description = '内容'

    list_display_links = ['question_id','abstract']
