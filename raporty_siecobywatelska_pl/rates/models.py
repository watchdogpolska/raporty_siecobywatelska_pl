from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from raporty_siecobywatelska_pl.institutions.models import Institution
from django.utils.translation import ugettext_lazy as _

from raporty_siecobywatelska_pl.questionnaire.models import Group
from raporty_siecobywatelska_pl.ranking.models import Ranking


@python_2_unicode_compatible
class Rate(models.Model):
    total_points = models.IntegerField(verbose_name=_("Total points"))
    collected_points = models.IntegerField(verbose_name=_("Collected points"))

    class Meta:
        abstract = True

    @property
    def value(self):
        return self.collected_points / self.total_points * 100

    def __str__(self):
        return "%s%%" % round(self.value)


@python_2_unicode_compatible
class InstitutionRankingRate(Rate):
    institution = models.ForeignKey(Institution, blank=False, related_name="institution_rates")
    ranking = models.ForeignKey(Ranking, blank=False, related_name="+")

    class Meta:
        verbose_name = _("Institution's rate")
        verbose_name_plural = _("Institutions rates")
        unique_together = ('institution', 'ranking',)


@python_2_unicode_compatible
class InstitutionGroupRate(Rate):
    institution = models.ForeignKey(Institution, blank=False, related_name="+")
    group = models.ForeignKey(Group, blank=False, related_name="groups_rates")

    class Meta:
        verbose_name = _("Groups's rates")
        verbose_name_plural = _("Institutions assessments")
        unique_together = ('institution', 'group',)
