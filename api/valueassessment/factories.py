from datetime import datetime

import factory.fuzzy
import pytz
from core.enums import GenericStatuses
from core.factories import UserFactory

from . import enums, models

factory.Faker._DEFAULT_LOCALE = 'en_US'


class ValueFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Value {n}")
    year = factory.fuzzy.FuzzyDate(
        datetime(2023, 1, 1), datetime(2023, 12, 31))
    role = factory.fuzzy.FuzzyChoice(enums.ValueRoles)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Value


class ValueItemFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Value {n}")
    proficiency = factory.fuzzy.FuzzyInteger(1, 9)
    description = factory.Sequence(lambda n: f"Description {n}")

    class Meta:
        model = models.ValueItem


class ValueAssessmentItemFactory(factory.django.DjangoModelFactory):
    score = factory.fuzzy.FuzzyInteger(1, 9)
    value_item = factory.SubFactory(ValueItemFactory)

    class Meta:
        model = models.ValueAssessmentItem


class ValueAssessmentFactory(factory.django.DjangoModelFactory):
    target_employee = factory.SubFactory(UserFactory)
    assigned_employee = factory.SubFactory(UserFactory)
    value = factory.SubFactory(ValueFactory)
    status = factory.fuzzy.FuzzyChoice(GenericStatuses)
    value_assessment_item = factory.SubFactory(ValueAssessmentItemFactory)
    type = factory.fuzzy.FuzzyChoice(enums.ValueAssessmentTypes)

    class Meta:
        model = models.ValueAssessment
