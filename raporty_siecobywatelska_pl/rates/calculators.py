from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Group
from django.db.models import Sum, Count

from raporty_siecobywatelska_pl.rates.models import InstitutionGroupRate, InstitutionExplorationRate


def refresh_groups_institution_rates(institution, exploration):
    groups = Group.objects.filter(exploration=exploration) \
        .filter(question__result__institution_id=institution) \
        .annotate(collected_points=Sum('question__result__option__value')) \
        .annotate(total_points=Count('question__answer'))
    import ipdb; ipdb.set_trace()
    # for group in groups:
    #     _save_or_update_rate(
    #         InstitutionGroupRate, group,
    #         group=group,
    #         institution=institution
    #     )


def refresh_exploration_institution_rates(institutions, exploration):
    institution_results = Institution.objects.filter(pk__in=institutions) \
        .annotate(collected_points=Sum('result__option__value')) \
        .annotate(total_points=Count('answer'))
    import ipdb; ipdb.set_trace()

    # for institution in institution_results:
    #     _save_or_update_rate(
    #         InstitutionExplorationRate,
    #         institution,
    #         institution=institution,
    #         exploration=exploration
    #     )


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
