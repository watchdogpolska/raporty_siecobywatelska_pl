from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator

from raporty_siecobywatelska_pl.exploration.models import Exploration
from django.db.models import Sum, Count

from raporty_siecobywatelska_pl.rates.calculators import refresh_exploration_institution_rates
from raporty_siecobywatelska_pl.rates.models import InstitutionExplorationRate


class Command(BaseCommand):
    help = 'Refresh a exploration institution rates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--exploration_id',
            action='store_true',
            dest='exploration_id',
            default=False,
            help='Specifies a specific exploration',
        )

    def handle(self, *args, **options):
        explorations_qs = Exploration.objects

        if options["exploration_id"]:
            explorations_qs = explorations_qs.filter(id=args)

        for exploration in explorations_qs.all():
            paginator = Paginator(exploration.institutions.all(), 50)
            for page in range(1, paginator.num_pages + 1):
                refresh_exploration_institution_rates(paginator.page(page).object_list, exploration)
                self.stdout.write("%s / %s" % (page, paginator.num_pages))
        self.stdout.write(self.style.SUCCESS('Successfully refreshed all rates'))
