import factory
import factory.fuzzy

from raporty_siecobywatelska_pl.ranking.models import Raport


class LetterFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence('title-letter-{0}'.format)
    description = factory.Sequence('quote-{0}'.format)

    class Meta:
        model = Raport
