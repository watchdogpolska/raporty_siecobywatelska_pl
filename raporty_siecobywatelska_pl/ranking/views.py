from audioop import reverse

from django.db.models import Count
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView, RedirectView

from raporty_siecobywatelska_pl.ranking import models
from raporty_siecobywatelska_pl.ranking.models import Ranking


class RankingRedirect(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return self.request.ranking.get_absolute_url()


class RankingList(ListView):
    model = models.Ranking
    paginate_by = 10


class RankingDetail(DetailView):
    model = models.Ranking
    slug_url_kwarg = "ranking_slug"

    def get_queryset(self):
        return super(RankingDetail, self).get_queryset()\
            .prefetch_related('group_set')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, stats=self.stats)

    @cached_property
    def stats(self):
        return Ranking.objects.filter(pk=self.request.ranking.pk)\
            .annotate(num_institution=Count('institutions'))\
            .annotate(num_article=Count('article'))\
            .annotate(num_group=Count('group')).first()


