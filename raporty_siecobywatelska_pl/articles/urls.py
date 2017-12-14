
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/articles/(?P<slug>[\w-]+)/$'),
        views.RankingArticleDetailView.as_view(),
        name="ranking-article-detail"
    ),
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/articles/$'),
        views.RankingArticleListView.as_view(),
        name="ranking-article-list"
    ),

]
