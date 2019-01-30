from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from raporty_siecobywatelska_pl.exploration.models import Exploration


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
    exploration = models.ForeignKey(
        to=Exploration,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Question group")
        verbose_name_plural = _("Question groups")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('questionnaire:exploration-group-detail', args=[self.exploration.slug, self.slug])

    def __str__(self):
        return self.name


class QuestionQuerySet(QuerySet):
    def for_exploration(self, exploration):
        return self.filter(group__exploration=exploration)


@python_2_unicode_compatible
class Question(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    description = HTMLField(verbose_name=_("Description"))

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Question")
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('exploration:detail', kwargs={'slug': self.group.exploration.slug})

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TextOption(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=250,
        verbose_name=_("Name")
    )
    value = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
    )

    def __str__(self):
        return self.name

