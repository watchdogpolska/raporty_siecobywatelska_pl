from django.core.management.base import BaseCommand, CommandError

from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Group
from raporty_siecobywatelska_pl.exploration.models import Exploration
from django.db.models import Sum, Count, Prefetch

from raporty_siecobywatelska_pl.rates.calculators import refresh_groups_institution_rates
from raporty_siecobywatelska_pl.rates.models import InstitutionExplorationRate, InstitutionGroupRate


class Command(BaseCommand):
    help = 'Refresh a group institution rates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--exploration_id',
            action='store_true',
            dest='exploration_id',
            default=False,
            help='Specifies a specific exploration',
        )

    def handle(self, *args, **options):
        exploration_qs = Exploration.objects
        if options["exploration_id"]:
            exploration_qs = exploration_qs.filter(id=args)

        for exploration in exploration_qs.all():
            for institution in exploration.institutions.all():
                refresh_groups_institution_rates(institution, exploration)
            self.stdout.write(
                'Refreshed rate for "%s" (id: %s)' % (str(institution), institution.pk))
        self.stdout.write(self.style.SUCCESS('Successfully refreshed all rates'))
