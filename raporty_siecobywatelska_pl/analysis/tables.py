from raporty_siecobywatelska_pl.institutions.tables import InstitutionView


class InstitutionCompareView(InstitutionView):
    def get_column_type(self, position):
        if position == 0:
            return "name"
        return "value"

    def get_column_count(self):
        return 1 + len(self.institutions)

    def get_column_context(self, column):
        context = super(InstitutionCompareView, self).get_column_context(column)
        if column != 0:
            context['institution'] = self.institutions[column - 1]
        return context

    def get_rows_count(self):
        return 1 + len(self.groups)

    def get_row_type(self, row):
        if row == 0:
            return "total"
        return "group"

    def get_row_context(self, row):
        context = super(InstitutionCompareView, self).get_row_context(row)
        if row != 0:
            context['group'] = self.groups[row - 1]
        return context

    def get_cell_context(self, row, column):
        context = super(InstitutionCompareView, self).get_cell_context(row, column)
        if column != 0:
            institution = self.institutions[column - 1]
            if row == 0:
                context['rate'] = self.get_institution_rate(institution)
                return context
            group = self.groups[row - 1]
            context['rate'] = self.get_group_institution_rate(group, institution)
        return context
