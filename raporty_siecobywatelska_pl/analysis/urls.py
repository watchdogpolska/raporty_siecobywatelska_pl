
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/analysis$'),
        views.AnalysisList.as_view(),
        name="analysis-list"
    ),
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/analysis/compare$'),
        views.ExplorationInstitutionCompareView.as_view(),
        name="analysis-institution"
    ),
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/analysis/grouping$'),
        views.ExplorationInstitutionGroupingView.as_view(),
        name="analysis-institution"
    ),
]
