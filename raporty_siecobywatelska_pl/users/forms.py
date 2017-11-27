from django import forms

from raporty_siecobywatelska_pl.users import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_group_wrapper_class = 'row'
        self.helper.wrapper_class = 'row'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.User
        fields = [
            'name'
         ]
