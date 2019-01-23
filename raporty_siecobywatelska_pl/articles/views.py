from django.views.generic import DetailView, ListView

from raporty_siecobywatelska_pl.articles.models import Article


class ExplorationArticleDetailView(DetailView):
    model = Article
    template_name = "articles/exploration_article_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(exploration=self.request.exploration)


class ExplorationArticleListView(ListView):
    model = Article
    template_name = "articles/exploration_article_list.html"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(exploration=self.request.exploration)
