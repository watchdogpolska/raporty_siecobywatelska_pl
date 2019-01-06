
from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/groups/(?P<slug>[\w-]+)/$'),
        views.ExplorationGroupDetailView.as_view(),
        name="exploration-group-detail"
    ),
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/groups/$'),
        views.ExplorationGroupListView.as_view(),
        name="exploration-group-list"
    ),

]
