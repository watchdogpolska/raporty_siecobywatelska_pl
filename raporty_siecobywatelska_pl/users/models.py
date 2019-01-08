from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField

from raporty_siecobywatelska_pl.institutions.models import Institution


@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    is_initially_introduced = models.BooleanField(_('It is initially introduced'), blank=False, default=False)
    score_of_credibility = models.IntegerField(default=100)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


@python_2_unicode_compatible
class AnswersCredibilityPoints(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    institution = models.ForeignKey(
        to=Institution,
        on_delete=models.CASCADE
    )
    exploration = models.ForeignKey(
        to=Institution,
        on_delete=models.CASCADE
    )
    created = CreationDateTimeField(
        verbose_name=_('created')
    )
    point = models.IntegerField()

    class Meta:
        unique_together = (
            'user',
            'institution',
            'exploration'
        )
