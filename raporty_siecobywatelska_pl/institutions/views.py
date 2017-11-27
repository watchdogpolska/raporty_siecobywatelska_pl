from dal import autocomplete
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from raporty_siecobywatelska_pl.institutions.filters import InstitutionFilter
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.ranking.models import Ranking
from raporty_siecobywatelska_pl.views import ExprAutocompleteMixin


class RankingInstitutionDetailView(DetailView):
    model = Institution

    def get_queryset(self):
        return super(RankingInstitutionDetailView, self)\
            .get_queryset().filter(rankings__slug=self.ranking.slug)

    def get_context_data(self, **kwargs):
        return super(RankingInstitutionDetailView, self).get_context_data(
            other_rankings=Ranking.objects.exclude(slug=self.ranking.slug),
            ranking=Ranking.objects.get(slug=self.ranking.slug),
            **kwargs
        )

    @cached_property
    def ranking(self):
        ranking_slug = self.kwargs['ranking_slug']
        return Ranking.objects.get(slug=ranking_slug)


class RankingInstitutionListView(FilterView):
    model = Institution
    filterset_class = InstitutionFilter
    paginate_by = 25

    def get_queryset(self):
        return super(RankingInstitutionListView, self)\
            .get_queryset().filter(rankings__slug=self.ranking.slug)

    def get_context_data(self, **kwargs):
        return super(RankingInstitutionListView, self).get_context_data(
            ranking=self.ranking,
            **kwargs
        )

    @cached_property
    def ranking(self):
        ranking_slug = self.kwargs['ranking_slug']
        return Ranking.objects.get(slug=ranking_slug)


class InstitutionAutocomplete(ExprAutocompleteMixin,
                          autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
    ]
    model = Institution
