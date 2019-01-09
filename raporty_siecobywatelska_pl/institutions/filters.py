import django_filters
from dal import autocomplete
from teryt_tree.dal_ext.filters import VoivodeshipFilter, CountyFilter, CommunityFilter

from raporty_siecobywatelska_pl.filters import CrispyFilterMixin
from raporty_siecobywatelska_pl.institutions.models import Institution
from django.utils.translation import ugettext as _


class InstitutionFilter(CrispyFilterMixin, django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    parents = django_filters.ModelChoiceFilter(
        queryset=Institution.objects.all(),
        widget=autocomplete.ModelSelect2(url='institutions:institution-autocomplete')
    )
    voivodeship = VoivodeshipFilter(
        label=_("Wojewódzctwo"),
        widget=autocomplete.ModelSelect2(url='teryt:voivodeship-autocomplete')
    )
    county = CountyFilter(
        label=_("Powiat"),
        widget=autocomplete.ModelSelect2(url='teryt:county-autocomplete',
                                         forward=['voivodeship'])
    )
    community = CommunityFilter(
        label=_("Gmina"),
        widget=autocomplete.ModelSelect2(url='teryt:community-autocomplete',
                                         forward=['county'])
    )

    class Meta:
        model = Institution
        fields = ['regon']
