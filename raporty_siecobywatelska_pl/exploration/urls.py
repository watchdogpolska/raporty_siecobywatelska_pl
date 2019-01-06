from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(_(r'^(?P<exploration_slug>[\w-]+)/?$'), views.ExplorationRedirect.as_view(), name="redirect"),
    url(_(r'^(?P<exploration_slug>[\w-]+)/information$'), views.ExplorationDetail.as_view(), name="detail"),
    url(_(r'^$'), views.ExplorationList.as_view(), name="list"),
]
