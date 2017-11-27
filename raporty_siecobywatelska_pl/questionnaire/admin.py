from django.contrib import admin

from .models import Group, Question


class GroupInline(admin.StackedInline):
    model = Group
    show_change_link = True


class QuestionInline(admin.StackedInline):
    model = Question
    show_change_link = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ranking')
    list_filter = ('ranking',)
    search_fields = ('name',)
    inlines = [
        QuestionInline
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)
