from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from tinymce.models import HTMLField

from raporty_siecobywatelska_pl.exploration.models import Exploration


def populate_slug(instance):
    return instance.name.lower()


class Article(TimeStampedModel):
    name = models.CharField(
        max_length=250,
        verbose_name=_("Name")
    )
    slug = AutoSlugField(
        populate_from=populate_slug,
        verbose_name=_("Slug"),
        unique=True
    )
    short_description = models.TextField(
        verbose_name=_("Short description")
    )
    description = HTMLField(
        verbose_name=_("Description")
    )
    exploration = models.ForeignKey(
        to=Exploration,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:exploration-article-detail', args=[self.exploration.slug, self.slug])

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['name']
