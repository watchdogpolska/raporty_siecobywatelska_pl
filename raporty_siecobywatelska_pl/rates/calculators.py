from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Group
from django.db.models import Sum, Count

from raporty_siecobywatelska_pl.rates.models import InstitutionGroupRate, InstitutionRankingRate


def refresh_groups_institution_rates(institution, ranking):
    groups = Group.objects.filter(ranking=ranking) \
        .filter(question__answer__institution_id=institution) \
        .annotate(collected_points=Sum('question__answer__value')) \
        .annotate(total_points=Count('question__answer'))
    for group in groups:
        _save_or_update_rate(
            InstitutionGroupRate, group,
            group=group,
            institution=institution
        )


def refresh_ranking_institution_rates(institutions, ranking):
    institution_results = Institution.objects.filter(pk__in=institutions) \
        .annotate(collected_points=Sum('answer__value')) \
        .annotate(total_points=Count('answer'))
    for institution in institution_results:
        _save_or_update_rate(
            InstitutionRankingRate,
            institution,
            institution=institution,
            ranking=ranking
        )


def _save_or_update_rate(cls, data, **lookup):
    try:
        rate = cls.objects.get(**lookup)
        if _is_dirty_rate(data, rate):
            rate.collected_points = data.collected_points
            rate.total_points = data.total_points
            rate.save()
    except cls.DoesNotExist:
        cls.objects.create(
            **lookup,
            collected_points=data.collected_points,
            total_points=data.total_points
        )


def _is_dirty_rate(group, rate):
    return rate.collected_points != group.collected_points \
           or rate.total_points != group.total_points
