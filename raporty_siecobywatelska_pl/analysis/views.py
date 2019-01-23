from django.views.generic import TemplateView

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
