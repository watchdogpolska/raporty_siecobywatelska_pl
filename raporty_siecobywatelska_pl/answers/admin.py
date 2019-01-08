from django.contrib import admin

from .models import Answer


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'value', 'note', 'institution', 'question')
#     list_filter = ('institution', 'question')
#     fields = (
#         'value',
#         'institution',
#         'question',
#         'note'
#     )
