from celery import shared_task
from django.core.mail import mail_managers

from raporty_siecobywatelska_pl.answers.models import Answer, Result
from raporty_siecobywatelska_pl.exploration.models import Exploration
from raporty_siecobywatelska_pl.institutions.models import Institution
from raporty_siecobywatelska_pl.questionnaire.models import Question
from raporty_siecobywatelska_pl.users.models import AnswersCredibilityPoints
from raporty_siecobywatelska_pl.users.tasks import recalculate_points
from raporty_siecobywatelska_pl.rates.tasks import refresh_rates

TOTAL_POINT_PER_QUESTIONNAIRE = 100



# [START listing_verify_answer]
@shared_task(name="answers:verify_result")
def verify_answers(exploration_id, institution_id):
    print("Start task: verify_answers for exploration_id=%s, institution_id=%s" % (exploration_id, institution_id))
    exploration = Exploration.objects.get(pk=exploration_id)
    institution = Institution.objects.get(pk=institution_id)
    questions = Question.objects.for_exploration(exploration)
    answers = Answer.objects.filter(
        question__group__exploration_id=exploration.id,
        institution_id=institution_id
    )
    Result.objects.filter(
        question__group__exploration_id=exploration.id,
        institution_id=institution_id
    ).delete()

    users = ({answer.user.id: answer.user for answer in answers}).values()
    sum_point_of_credibility = sum([user.score_of_credibility for user in users])

    if sum_point_of_credibility < exploration.requirement_of_credibility:
        print("Kryterium puntkowe nie osiągnietę. Pomijanie")
        return

    total_user_points = {user.id: 0 for user in users}
    point_per_question = TOTAL_POINT_PER_QUESTIONNAIRE / len(questions)
    for question in questions:

        most_common_options_id = most_common([
            answer.option.id for answer in answers if answer.question_id == question.pk
        ])

        current_user_points = calculate_user_points_for_question(answers, 
                                                                 most_common_options_id, 
                                                                 question, point_per_question, users)
        total_user_points = sum_user_points(current_user_points, total_user_points)
        Result(
            option_id=most_common_options_id,
            question_id=question.id,
            institution_id=institution_id
        ).save()

    save_user_points(exploration, exploration_id, institution, institution_id, total_user_points, users)

    recalculate_points.delay([user.pk for user in users])
    refresh_rates.delay(exploration.pk)

    send_admin_notification(exploration_id, institution_id)
    print("Finished verify_answers")
# [END listing_verify_answer]

def send_admin_notification(exploration_id, institution_id):
    mail_managers(
        subject="A new result for institutions",
        message=f"Institution ID: {institution_id}\nexploration ID: {exploration_id}",
        fail_silently=False
    )


def save_user_points(exploration, exploration_id, institution, institution_id, total_user_points, users):
    credibility_points = AnswersCredibilityPoints.objects.filter(
        exploration_id=exploration_id,
        institution_id=institution_id
    ).all()
    credibility_point_users_id = set(point.user.id for point in credibility_points)
    for user in users:
        if user.id in credibility_point_users_id:
            print("Uzytkownik %s juz dostał za ten kwestionariusz punkty" % (user.id))
            continue

        AnswersCredibilityPoints(
            user=user,
            institution=institution,
            exploration=exploration,
            point=total_user_points[user.pk]
        ).save()


def sum_user_points(current_user_points, total_user_points):
    return {user.id: current_user_points[user.id] + total_user_points for user in total_user_points}


def calculate_user_points_for_question(answers, most_common_options_id, question, point_per_question, users):
    user_points = {user.id: 0 for user in users}
    print("For question id: %s most common option id is %s" % (question.pk, most_common_options_id))

    for user in users:
        user_answer = next(answer for answer in answers if answer.user_id == user.pk)
        if user_answer is not None and user_answer.option_id != most_common_options_id:
            print("User %s received %s points" % (user.id, most_common_options_id))
            point_for_user = point_per_question
        else:
            print("User %s lost %s points" % (user.id, most_common_options_id))

            point_for_user = -point_per_question

        user_points[user.id] += point_for_user
    return user_points


def most_common(lst):
    return max(set(lst), key=lst.count)
