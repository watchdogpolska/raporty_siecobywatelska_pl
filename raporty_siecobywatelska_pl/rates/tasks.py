from celery import shared_task
from django.core.paginator import Paginator

from raporty_siecobywatelska_pl.exploration.models import Exploration
from raporty_siecobywatelska_pl.rates.calculators import refresh_groups_institution_rates, \
    refresh_exploration_institution_rates


@shared_task(name="rates:refresh_rates")
def refresh_rates(exploration_id):
    exploration = Exploration.objects.filter(id=exploration_id).first()

    for institution in exploration.institutions.all():
        refresh_groups_institution_rates(institution, exploration)

    paginator = Paginator(exploration.institutions.all(), 50)
    for page in range(1, paginator.num_pages + 1):
        institutions = paginator.page(page).object_list
        refresh_exploration_institution_rates(institutions, exploration)
