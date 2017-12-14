from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from raporty_siecobywatelska_pl.ranking.models import Ranking
from raporty_siecobywatelska_pl.articles.models import Article


class RankingArticleDetailView(DetailView):
    model = Article
    template_name = "articles/ranking_article_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(ranking=self.request.ranking)


class RankingArticleListView(ListView):
    model = Article
    template_name = "articles/ranking_article_list.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(ranking=self.request.ranking)
