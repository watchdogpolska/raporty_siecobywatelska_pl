import factory

from raporty_siecobywatelska_pl.teryt.factory import JSTFactory
from raporty_siecobywatelska_pl.teryt.models import JST
from .models import Institution


class InstitutionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence('institution-{0}'.format)
    jst = factory.Iterator(JST.objects.community().all())
    email = factory.Sequence('email-{0}@example.com'.format)

    class Meta:
        model = Institution
