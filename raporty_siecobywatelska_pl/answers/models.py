from django.db import models
from raporty_siecobywatelska_pl.institutions.models import Institution

from raporty_siecobywatelska_pl.questionnaire.models import Question, TextOption
from raporty_siecobywatelska_pl.users.models import User


class Answer(models.Model):
    option = models.ForeignKey(
        to=TextOption,
        on_delete=models.CASCADE
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            'institution',
            'question',
            'user'
        )


class Result(models.Model):
    option = models.ForeignKey(
        to=TextOption,
        on_delete=models.CASCADE
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            'institution',
            'question',
        )
