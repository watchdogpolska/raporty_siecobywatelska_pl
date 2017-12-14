from django.core.management.base import BaseCommand, CommandError

from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Group
from raporty_siecobywatelska_pl.ranking.models import Ranking
from django.db.models import Sum, Count, Prefetch

from raporty_siecobywatelska_pl.rates.calculators import refresh_groups_institution_rates
from raporty_siecobywatelska_pl.rates.models import InstitutionRankingRate, InstitutionGroupRate


class Command(BaseCommand):
    help = 'Refresh a group institution rates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ranking_id',
            action='store_true',
            dest='ranking_id',
            default=False,
            help='Specifies a specific ranking',
        )

    def handle(self, *args, **options):
        rankings_qs = Ranking.objects
        if options["ranking_id"]:
            rankings_qs = rankings_qs.filter(id=args)

        for ranking in rankings_qs.all():
            for institution in ranking.institutions.all():
                refresh_groups_institution_rates(institution, ranking)
            self.stdout.write(
                'Refreshed rate for "%s" (id: %s)' % (str(institution), institution.pk))
        self.stdout.write(self.style.SUCCESS('Successfully refreshed all rates'))
