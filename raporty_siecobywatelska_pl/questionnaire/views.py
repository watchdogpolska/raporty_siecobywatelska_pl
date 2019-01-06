from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from raporty_siecobywatelska_pl.questionnaire.models import Group
from raporty_siecobywatelska_pl.rates.models import InstitutionGroupRate


class ExplorationGroupDetailView(DetailView):
    model = Group
    template_name = "questionnaire/exploration_group_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(exploration=self.request.exploration)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            exploration=self.request.exploration,
            institution_group_rate=self.institution_group_rate,
            **kwargs)

    @cached_property
    def institution_group_rate(self):
        return InstitutionGroupRate.objects\
            .filter(group=self.object)\
            .order_by("-collected_points")\
            .select_related('institution')\
            .all()[:10]


class ExplorationGroupListView(ListView):
    model = Group
    template_name = "questionnaire/exploration_group_list.html"
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset()\
            .filter(exploration=self.request.exploration)
