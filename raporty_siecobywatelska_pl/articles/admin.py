# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'ranking',
        'name',
        'short_description',
        'description',
    )
    list_filter = ('ranking',)
    search_fields = ('name',)
