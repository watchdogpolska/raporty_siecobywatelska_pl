from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView

from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.ranking.models import Ranking


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


class RankingInstitutionListView(ListView):
    model = Institution
    paginate_by = 25

    def get_queryset(self):
        ranking_slug = self.kwargs['ranking_slug']
        return super(RankingInstitutionListView, self)\
            .get_queryset().filter(rankings__slug=ranking_slug)

    def get_context_data(self, **kwargs):
        ranking_slug = self.kwargs['ranking_slug']
        return super(RankingInstitutionListView, self).get_context_data(
            ranking=Ranking.objects.get(slug=ranking_slug),
            **kwargs
        )
