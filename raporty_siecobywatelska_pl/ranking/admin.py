from django.contrib import admin

from raporty_siecobywatelska_pl.questionnaire.admin import GroupInline
from .models import Ranking


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    list_filter = ('created', 'modified')
    raw_id_fields = ('institutions',)
    search_fields = ('name',)
    inlines = [
        GroupInline
    ]

