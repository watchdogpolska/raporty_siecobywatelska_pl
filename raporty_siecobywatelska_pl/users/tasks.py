from celery import shared_task

from raporty_siecobywatelska_pl.users.models import AnswersCredibilityPoints, User


@shared_task(name="users:recalculate_points")
def recalculate_points(users_ids):
    print("recalculate_points for users_ids= %s" % users_ids)
    users = User.objects.filter(id__in=users_ids)
    for user in users:
        crediiblity_points = AnswersCredibilityPoints.objects.filter(user=user).all()
        score_of_credibility = sum([point.point for point in crediiblity_points])
        print("User %s has total score: %s" % (users_ids, score_of_credibility))
        user.score_of_credibility = score_of_credibility
        user.save()
    print("Finished recalculate_points")
