from django.db import models
from django.utils.translation import ugettext_lazy as _

from raporty_siecobywatelska_pl.institutions.models import Institution
from django.core.validators import MaxValueValidator, MinValueValidator

from raporty_siecobywatelska_pl.questionnaire.models import Question


class Answer(models.Model):
    value = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
        verbose_name=_("Value")
    )
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('institution', 'question',)
