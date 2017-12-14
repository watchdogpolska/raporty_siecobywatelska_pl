class BaseView(object):
    def get_table(self):
        return {
            "headings": self.get_headings(),
            "body": self.get_rows(),
        }

    # Type
    def get_column_type(self, column):
        return "plain"

    def get_row_type(self, row):
        return "plain"

    # Heading
    def get_headings(self):
        return [self.get_heading(i) for i in range(self.get_column_count())]

    def get_heading(self, position):
        return self._merge_dicts(
            {"column_type": self.get_column_type(position)},
            self.get_column_context(position)
        )

    # Row
    def get_rows(self):
        return [self.get_row(row) for row in range(0, self.get_rows_count())]

    def get_row(self, row):
        return [self.get_cell_context(row, column) for column in range(0, self.get_column_count())]

    # Count
    def get_column_count(self):
        return 0

    def get_rows_count(self):
        return 0

    # Context
    def get_row_context(self, row):
        return {
            "row_type": self.get_row_type(row)
        }

    def get_column_context(self, column):
        return {"column_type": self.get_column_type(column)}

    def get_cell_context(self, row, column):
        context = {}
        context.update(self.get_column_context(column))
        context.update(self.get_row_context(row))
        return context

    @staticmethod
    def _merge_dicts(*dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result
