from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/institution/(?P<slug>[\w-]+)/$'),
        views.RankingInstitutionDetailView.as_view(),
        name="ranking-detail"
    ),
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/institution/$'),
        views.RankingInstitutionListView.as_view(),
        name="ranking-list"
    ),
]
