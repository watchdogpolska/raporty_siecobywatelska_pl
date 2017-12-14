from dal import autocomplete
from django.db.models import Prefetch
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from raporty_siecobywatelska_pl.answers.models import Answer
from raporty_siecobywatelska_pl.institutions.filters import InstitutionFilter
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.institutions.tables import InstitutionFilterTableView
from raporty_siecobywatelska_pl.questionnaire.models import Group, Question
from raporty_siecobywatelska_pl.ranking.models import Ranking
from raporty_siecobywatelska_pl.rates.models import InstitutionGroupRate, InstitutionRankingRate
from raporty_siecobywatelska_pl.views import ExprAutocompleteMixin


class RankingInstitutionDetailView(DetailView):
    model = Institution
    template_name = "institutions/ranking_institution_detail.html"

    def get_queryset(self):
        return super(RankingInstitutionDetailView, self)\
            .get_queryset().filter(rankings=self.request.ranking)

    def get_context_data(self, **kwargs):
        return super(RankingInstitutionDetailView, self).get_context_data(
            other_rankings=self.other_related_ranking,
            table_data=self.get_table_data(),
            institution_rate=self.institution_rate,
            **kwargs
        )

    def get_table_data(self):
        groups = self.question_groups

        return [{
                'group': group,
                'rate': group.rates[0] if len(group.rates) > 0 else None,
                'questions': [
                    {
                        'question': question,
                        'answer': question.answers[0] if len(question.answers) > 0 else None
                    } for question in group.questions]
            } for group in groups]


    @cached_property
    def institution_rate(self):
        return InstitutionRankingRate.objects.filter(
            ranking=self.request.ranking,
            institution=self.object
        ).first()

    @cached_property
    def question_groups(self):
        qs_answer = Answer.objects.filter(institution=self.object)
        qs_question = Question.objects.prefetch_related(
            Prefetch('answer_set', queryset=qs_answer, to_attr='answers')
        )

        return Group.objects.filter(ranking=self.request.ranking)\
            .prefetch_related(
                Prefetch(
                    'question_set',
                    queryset=qs_question,
                    to_attr='questions'
                ),
                Prefetch(
                    'groups_rates',
                    queryset=InstitutionGroupRate.objects.filter(institution=self.object),
                    to_attr='rates'
                )
        )

    @cached_property
    def other_related_ranking(self):
        return Ranking.objects.exclude(pk=self.request.ranking.pk).all()


class RankingInstitutionListView(FilterView):
    model = Institution
    filterset_class = InstitutionFilter
    paginate_by = 25
    template_name = "institutions/ranking_institution_filter.html"

    def get_queryset(self):
        return super(RankingInstitutionListView, self)\
            .get_queryset().filter(rankings__slug=self.request.ranking.slug)\


    def get_context_data(self, **kwargs):
        # import ipdb; ipdb.set_trace()
        return super(RankingInstitutionListView, self).get_context_data(
            table=self.get_table_view().get_table(),
            **kwargs
        )

    def get_table_view(self):
        return InstitutionFilterTableView(self.request.ranking, self.object_list)


class InstitutionAutocomplete(ExprAutocompleteMixin,
                          autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
    ]
    model = Institution
