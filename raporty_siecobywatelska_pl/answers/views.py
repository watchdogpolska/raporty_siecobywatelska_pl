from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms
from django.db.models import Model
from django.forms import modelformset_factory, modelform_factory, formset_factory, \
    inlineformset_factory, BaseFormSet, ModelForm, BaseInlineFormSet
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from raporty_siecobywatelska_pl.answers.models import Answer

from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Question


class AnswerForm(forms.ModelForm):
    value = forms.IntegerField(min_value=-2, max_value=2)
    note = forms.TextInput()

    class Meta:
        model = Answer
        fields = (
            'value',
            'note'
        )


# AnswerForm = modelform_factory(Answer, fields=("value", "note"))


class AnswerFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AnswerFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Fieldset(
                '{{formset_form.instance.question}}',
                'value',
                'note'
            )
        )
        self.add_input(Submit("submit", "Save"))
        self.render_required_fields = True


class AnswerFormSet(BaseInlineFormSet):
    model = Answer
    parent_model = Institution
    fk = Answer.institution.field
    form = AnswerForm
    fields = ("value", "note")
    can_delete = False
    extra = 0
    min_num = 1
    max_num = 10
    can_order = False
    absolute_max = 50
    save_as_new = True
    validate_max = False
    validate_min = False

    def __init__(self, questions, **kwargs):
        super().__init__(**kwargs)
        self.questions = questions

    def total_form_count(self):
        return len(self.questions)

    def get_form_kwargs(self, index):
        kwargs = super(AnswerFormSet, self).get_form_kwargs(index=index)

        try:
            answer = Answer.objects.get(institution=self.instance, question=self.questions[index])
        except Answer.DoesNotExist:
            answer = Answer(institution=self.instance, question=self.questions[index])

        kwargs['instance'] = answer
        return kwargs

    def save(self, commit=True):
        instances = [form.instance for form in self.forms]
        for instance in instances:
            instance.save()
        return instances

# class AnswerFormSetHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super(AnswerFormSetHelper, self).__init__(*args, **kwargs)
#         self.form_method = 'post'
#         self.render_required_fields = True


class AnswerSaveView(TemplateView):

    template_name = "answers/answers_save.html"

    @cached_property
    def institution(self):
        institution_slug = self.kwargs['institution_slug']
        return Institution.objects.get(slug=institution_slug)

    @cached_property
    def questions(self):
        ranking_slug = self.kwargs['ranking_slug']
        return Question.objects.filter(group__ranking__slug=ranking_slug)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # import ipdb; ipdb.set_trace()
        return self.render_to_response(context)

    def get_formset(self):
        return AnswerFormSet(
            **self.get_formset_kwargs()
        )

    def post(self, *args, **kwargs):
        formset = self.get_formset()
        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.institution,
            'questions': self.questions
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AnswerSaveView, self).get_context_data(**kwargs)

        context.update({
            'formset': self.get_formset(),
            'institution': self.institution,
            'questions': self.questions,
            'helper': AnswerFormSetHelper()
        })
        return context

    def formset_invalid(self, formset):
        context = self.get_context_data()
        return self.render_to_response(context)

    def formset_valid(self, formset):
        formset.save()

        context = self.get_context_data()
        return self.render_to_response(context)
