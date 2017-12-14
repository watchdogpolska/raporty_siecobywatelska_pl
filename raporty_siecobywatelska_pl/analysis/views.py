from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView

from raporty_siecobywatelska_pl.analysis.tables import InstitutionCompareView
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.ranking.models import Ranking


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
