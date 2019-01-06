from django.contrib import admin

from raporty_siecobywatelska_pl.questionnaire.admin import GroupInline
from .models import Exploration


@admin.register(Exploration)
class ExplorationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('created', 'modified')
    raw_id_fields = ('institutions',)
    search_fields = ('name',)
    inlines = [
        GroupInline
    ]

