from __future__ import unicode_literals

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    url(
        _(r'^(?P<ranking_slug>[\w-]+)/institution/(?P<institution_slug>[\w-]+)/response/$'),
        views.AnswerSaveView.as_view(),
        name="save_answer"
    ),
]
