from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator

from raporty_siecobywatelska_pl.ranking.models import Ranking
from django.db.models import Sum, Count

from raporty_siecobywatelska_pl.rates.calculators import refresh_ranking_institution_rates
from raporty_siecobywatelska_pl.rates.models import InstitutionRankingRate


class Command(BaseCommand):
    help = 'Refresh a ranking institution rates'

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
            paginator = Paginator(ranking.institutions.all(), 50)
            for page in range(1, paginator.num_pages + 1):
                refresh_ranking_institution_rates(paginator.page(page).object_list, ranking)
                self.stdout.write("%s / %s" % (page, paginator.num_pages))
        self.stdout.write(self.style.SUCCESS('Successfully refreshed all rates'))
