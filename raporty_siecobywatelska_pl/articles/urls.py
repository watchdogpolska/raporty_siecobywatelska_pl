
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/articles/(?P<slug>[\w-]+)/$'),
        views.ExplorationArticleDetailView.as_view(),
        name="exploration-article-detail"
    ),
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/articles/$'),
        views.ExplorationArticleListView.as_view(),
        name="exploration-article-list"
    ),

]
