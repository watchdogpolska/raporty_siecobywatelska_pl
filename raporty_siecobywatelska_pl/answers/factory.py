import random

import factory

from raporty_siecobywatelska_pl.answers import models
from raporty_siecobywatelska_pl.institutions.factory import InstitutionFactory
from raporty_siecobywatelska_pl.questionnaire.factory import QuestionFactory


class AnswerFactory(factory.django.DjangoModelFactory):
    value = factory.LazyAttribute(lambda o: random.randint(-2, 2))
    note = factory.Sequence('user-{0}'.format)
    # TODO: Ensure that the institution exists in the exploration
    institution = factory.SubFactory(InstitutionFactory)
    question = factory.SubFactory(
        QuestionFactory
    )

    class Meta:
        model = models.Answer
