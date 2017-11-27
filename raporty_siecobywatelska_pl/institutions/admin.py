from django.contrib import admin

from .models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'jst',
        'regon',
    )
    list_filter = ('created', 'modified', 'jst')
    raw_id_fields = ('parents',)
    search_fields = ('name', 'slug')
