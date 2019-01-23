from django.contrib import admin

from .models import Group, Question, TextOption


class GroupInline(admin.StackedInline):
    model = Group
    show_change_link = True


class QuestionInline(admin.StackedInline):
    model = Question
    show_change_link = True


class TextOptionInline(admin.StackedInline):
    model = TextOption
    show_change_link = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'exploration')
    list_filter = ('exploration',)
    search_fields = ('name',)
    inlines = [
        QuestionInline
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)
    inlines = [
        TextOptionInline
    ]


@admin.register(TextOption)
class TextOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'name', 'value')
    list_filter = ('question',)
    search_fields = ('name',)
