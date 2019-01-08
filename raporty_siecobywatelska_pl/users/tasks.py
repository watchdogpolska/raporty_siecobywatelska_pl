from celery import shared_task

from raporty_siecobywatelska_pl.users.models import AnswersCredibilityPoints


@shared_task(name="users:recalculate_points")
def recalculate_points(users):
    for user in users:
        # TODO: Move to SQL
        crediiblity_points = AnswersCredibilityPoints.objects.filter(user=user).all()
        score_of_credibility = sum([point.value for point in crediiblity_points])
        user.score_of_credibility = score_of_credibility
        user.save(["score_of_credibility"])
