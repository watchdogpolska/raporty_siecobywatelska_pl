import factory

from raporty_siecobywatelska_pl.questionnaire.models import Group, Question


class QuestionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence('title-question-{0}'.format)
    description = factory.Sequence('description-{0}'.format)

    group = factory.SubFactory('raporty_siecobywatelska_pl.questionnaire.factory.GroupFactory')

    class Meta:
        model = Question


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence('name-group-{0}'.format)
    description = factory.Sequence('description-{0}'.format)
    exploration = factory.SubFactory('raporty_siecobywatelska_pl.exploration.factory.ExplorationFactory')

    question_1 = factory.RelatedFactory(QuestionFactory, "group")
    question_2 = factory.RelatedFactory(QuestionFactory, "group")
    question_3 = factory.RelatedFactory(QuestionFactory, "group")

    class Meta:
        model = Group




