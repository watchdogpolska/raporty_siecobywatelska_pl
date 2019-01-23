from audioop import reverse

from django.db.models import Count, OuterRef, Subquery, F
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView, RedirectView

from raporty_siecobywatelska_pl.articles.models import Article
from raporty_siecobywatelska_pl.exploration import models
from raporty_siecobywatelska_pl.questionnaire.models import Group


class ExplorationRedirect(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return self.request.exploration.get_absolute_url()


class ExplorationList(ListView):
    model = models.Exploration
    paginate_by = 10


class ExplorationDetail(DetailView):
    model = models.Exploration
    slug_url_kwarg = "exploration_slug"

    def get_queryset(self):
        return super(ExplorationDetail, self).get_queryset()\
            .prefetch_related('group_set')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, stats=self.stats)

    @cached_property
    def stats(self):
        return models.Exploration.objects.filter(pk=self.request.exploration.pk)\
            .annotate(num_institution=Count('institutions'))\
            .annotate(
                num_article=Subquery(
                    Article.objects
                    .filter(exploration=OuterRef('pk'))\
                    .order_by()
                    .values('exploration')\
                    .annotate(count=Count('exploration'))\
                    .values('count')[:1]
                )
            )\
            .annotate(num_group=Subquery(
                    Group.objects
                    .filter(exploration=OuterRef('pk')) \
                    .order_by()
                    .values('exploration')\
                    .annotate(count=Count('exploration'))\
                    .values('count')[:1]
            ))\
            .first()

# .annotate(num_institution=Count('institutions'))\
