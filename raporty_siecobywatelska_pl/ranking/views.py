from django.views.generic import ListView, DetailView

from raporty_siecobywatelska_pl.ranking import models


class RankingList(ListView):
    model = models.Ranking
    paginate_by = 5


class RankingDetail(DetailView):
    model = models.Ranking

    def get_queryset(self):
        return super(RankingDetail, self).get_queryset().prefetch_related('group_set')
