from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/institution/(?P<slug>[\w-]+)/$'),
        views.ExplorationInstitutionDetailView.as_view(),
        name="exploration-detail"
    ),
    url(
        _(r'^(?P<exploration_slug>[\w-]+)/institution/$'),
        views.ExplorationInstitutionListView.as_view(),
        name="exploration-list"
    ),
    url(
        _(r'^institution/autocomplete$'),
        views.InstitutionAutocomplete.as_view(),
        name="institution-autocomplete"
    ),
]
