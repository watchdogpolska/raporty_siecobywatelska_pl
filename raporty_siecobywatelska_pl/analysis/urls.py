
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/analysis$'),
        views.AnalysisList.as_view(),
        name="analysis-list"
    ),
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/analysis/institution$'),
        views.RankingInstitutionCompareView.as_view(),
        name="analysis-institution"
    ),

]
