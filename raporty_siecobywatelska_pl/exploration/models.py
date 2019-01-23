from autoslug import AutoSlugField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from teryt_tree.models import JednostkaAdministracyjna
from django.core.urlresolvers import reverse

from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.teryt.models import JST
from django.utils.translation import ugettext_lazy as _
from django.urls import resolve


class ExplorationManager(models.Manager):
    def get_current(self, request):
        resolver_match = request.resolver_match if request.resolver_match else resolve(request.path)

        if 'exploration_slug' in resolver_match.kwargs:
            exploration_slug = resolver_match.kwargs['exploration_slug']
            return self.get(slug=exploration_slug)
        return None


@python_2_unicode_compatible
class Exploration(TimeStampedModel):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    description = models.TextField()
    institutions = models.ManyToManyField(Institution, blank=True, related_name="explorations")
    requirement_of_credibility = models.IntegerField(default=200)
    objects = ExplorationManager()

    class Meta:
        verbose_name = _("Exploration")
        verbose_name_plural = _("Explorations")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('exploration:detail', kwargs={'exploration_slug': self.slug})

    def get_institutions_url(self):
        return reverse('institutions:exploration-list', kwargs={'exploration_slug': self.slug})

    def __str__(self):
        return self.name

