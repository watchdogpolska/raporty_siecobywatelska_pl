from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from teryt_tree.models import JednostkaAdministracyjna

from raporty_siecobywatelska_pl.teryt.models import JST
from django.utils.translation import ugettext_lazy as _


class InstitutionQuerySet(models.QuerySet):

    def area(self, jst):
        return self.filter(
            jst__tree_id=jst.tree_id,
            jst__lft__range=(jst.lft, jst.rght)
        )


@python_2_unicode_compatible
class Institution(TimeStampedModel):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    jst = models.ForeignKey(JST,
                            verbose_name=_('Unit of administrative division'),
                            db_index=True)
    regon = models.CharField(max_length=14, verbose_name=_("REGON number"), unique=True, null=True, blank=True)
    parents = models.ManyToManyField('self', verbose_name=_("Parent institutions"), blank=True)
    email = models.EmailField(verbose_name=_("Email of institution"))
    objects = InstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institution")
        ordering = ['name']

    def __str__(self):
        return self.name
