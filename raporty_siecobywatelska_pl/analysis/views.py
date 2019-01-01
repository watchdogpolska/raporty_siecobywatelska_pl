from django import forms
from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView

from raporty_siecobywatelska_pl.analysis.tables import InstitutionCompareView
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.ranking.models import Ranking
from raporty_siecobywatelska_pl.rates.models import InstitutionRankingRate


class RankingInstitutionCompareView(TemplateView):
    template_name = "analysis/ranking_institution_compare.html"

    def get_queryset(self):
        return Institution.objects.filter(rankings__slug=self.request.ranking.slug)

    def get_context_data(self, **kwargs):
        return super(RankingInstitutionCompareView, self).get_context_data(
            ranking=self.request.ranking,
            table=self.get_table_view().get_table(),
            **kwargs
        )

    def get_table_view(self):
        return InstitutionCompareView(self.request.ranking, self.get_queryset())


class AnalysisList(TemplateView):
    template_name = "analysis/analysis_list.html"


class RankingInstitutionGroupingView(TemplateView):
    template_name = 'analysis/analysis_grouping.html'

    def get_context_data(self, **kwargs):
        rates = InstitutionRankingRate.objects.group_by('institution__', 'author').filter(ranking=self.request.ranking)
        return super().get_context_data(rates=rates, **kwargs)
