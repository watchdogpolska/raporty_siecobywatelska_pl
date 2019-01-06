from django import forms
from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView

from raporty_siecobywatelska_pl.analysis.tables import InstitutionCompareView
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.exploration.models import Exploration
from raporty_siecobywatelska_pl.rates.models import InstitutionExplorationRate


class ExplorationInstitutionCompareView(TemplateView):
    template_name = "analysis/exploration_institution_compare.html"

    def get_queryset(self):
        return Institution.objects.filter(explorations__slug=self.request.exploration.slug)

    def get_context_data(self, **kwargs):
        return super(ExplorationInstitutionCompareView, self).get_context_data(
            exploration=self.request.exploration,
            table=self.get_table_view().get_table(),
            **kwargs
        )

    def get_table_view(self):
        return InstitutionCompareView(self.request.exploration, self.get_queryset())


class AnalysisList(TemplateView):
    template_name = "analysis/analysis_list.html"


class ExplorationInstitutionGroupingView(TemplateView):
    template_name = 'analysis/analysis_grouping.html'

    def get_context_data(self, **kwargs):
        rates = InstitutionExplorationRate.objects.group_by('institution__', 'author').filter(exploration=self.request.exploration)
        return super().get_context_data(rates=rates, **kwargs)
