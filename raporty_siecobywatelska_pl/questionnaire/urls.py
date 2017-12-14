
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/groups/(?P<slug>[\w-]+)/$'),
        views.RankingGroupDetailView.as_view(),
        name="ranking-group-detail"
    ),
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/groups/$'),
        views.RankingGroupListView.as_view(),
        name="ranking-group-list"
    ),

]
