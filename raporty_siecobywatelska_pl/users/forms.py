from django import forms

from raporty_siecobywatelska_pl.users import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.User
        fields = [
            'name'
         ]
