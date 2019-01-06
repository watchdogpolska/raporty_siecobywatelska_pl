from django.utils.functional import cached_property

from raporty_siecobywatelska_pl.questionnaire.models import Group
from raporty_siecobywatelska_pl.rates.models import InstitutionGroupRate, InstitutionExplorationRate
from raporty_siecobywatelska_pl.tables import BaseView


class InstitutionView(BaseView):
    def __init__(self, exploration, institutions):
        super().__init__()
        self.institutions = institutions
        self.exploration = exploration

    def get_institution_rate(self, institution):
        rate = (
            rate for rate in self.institution_rates if rate.institution_id == institution.pk
        )
        try:
            return next(rate)
        except StopIteration:
            pass
        return None

    def get_group_institution_rate(self, group, institution):
        rate = (rate for rate in self.group_rates if
              rate.group_id == group.pk and rate.institution_id == institution.pk)
        try:
            return next(rate)
        except StopIteration:
            pass
        return None

    @cached_property
    def groups(self):
        return Group.objects.filter(exploration=self.exploration).all()

    @cached_property
    def group_rates(self):
        return InstitutionGroupRate.objects.filter(institution__in=self.institutions)\
            .filter(group__in=self.groups).all()

    @cached_property
    def institution_rates(self):
        return InstitutionExplorationRate.objects.filter(exploration=self.exploration)\
            .filter(institution__in=self.institutions).all()


class InstitutionFilterTableView(InstitutionView):
    def get_column_count(self):
        return 1 + len(self.groups) + 1

    def get_column_type(self, position):
        if position == 0:
            return "name"
        position = position - 1
        if position < len(self.groups):
            return "group"
        return "exploration"

    def get_rows_count(self):
        return len(self.institutions)

    def get_column_context(self, column):
        context = super(InstitutionFilterTableView, self).get_column_context(column)
        column_type = self.get_column_type(column)
        if column_type == "group":
            context["group"] = self.groups[column - 1]
        if column_type == "exploration":
            context["exploration"] = self.exploration
        return context

    def get_row_context(self, row):
        context = super(InstitutionFilterTableView, self).get_row_context(row)
        context["institution"] = self.institutions[row]
        return context

    def get_cell_context(self, row, column):
        context = super(InstitutionFilterTableView, self).get_cell_context(row, column)
        column_type = self.get_column_type(column)
        institution = self.institutions[row]
        if column_type == "group":
            group = self.groups[column - 1]
            context["rate"] = self.get_group_institution_rate(group, institution)
        if column_type == "exploration":
            context["rate"] = self.get_institution_rate(institution)
        return context
