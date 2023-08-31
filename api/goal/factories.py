from datetime import datetime

import factory.fuzzy
import pytz
from core.factories import UserFactory
from core.enums import GenericStatuses
from . import enums, models

factory.Faker._DEFAULT_LOCALE = 'en_US'


class MoonshotFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Moonshot {n}")
    note = "Test"
    is_succeed = False

    class Meta:
        model = models.Moonshot


class HandshakeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Handshake {n}")
    note = "Test"
    is_succeed = False

    class Meta:
        model = models.Handshake


class GoalFactory(factory.django.DjangoModelFactory):
    employee = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText(length=50)
    quarter = factory.fuzzy.FuzzyChoice(enums.Quarters)
    year = factory.fuzzy.FuzzyDate(
        datetime(2023, 7, 16), datetime(2023, 7, 17))
    status = factory.fuzzy.FuzzyChoice(GenericStatuses)
    created_at = factory.fuzzy.FuzzyDateTime(
        (datetime(2023, 7, 16, tzinfo=pytz.UTC)))
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Goal

    @factory.post_generation
    def moonshots(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for shot in extracted:
                self.moonshots.add(shot)

    @factory.post_generation
    def handshakes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for handshake in extracted:
                self.handshakes.add(handshake)
