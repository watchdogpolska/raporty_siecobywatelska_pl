# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'exploration',
        'name',
        'short_description',
        'description',
    )
    list_filter = ('exploration',)
    search_fields = ('name',)
