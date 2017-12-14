from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from raporty_siecobywatelska_pl.ranking.models import Ranking


@python_2_unicode_compatible
class Group(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name=_("Name")
    )
    description = HTMLField(
        verbose_name=_("Description")
    )
    slug = AutoSlugField(
        populate_from='name',
        verbose_name=_("Slug"),
        unique=True
    )
    ranking = models.ForeignKey(
        to=Ranking,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Question group")
        verbose_name_plural = _("Question groups")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('questionnaire:ranking-group-detail', args=[self.ranking.slug, self.slug])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Question(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    description = HTMLField(verbose_name=_("Description"))

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Question")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('rankings:detail', kwargs={'slug': self.group.ranking.slug})

    def __str__(self):
        return self.name
