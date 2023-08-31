import factory.fuzzy
from core import enums, models, services


class DepartmentFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Department {n}")

    class Meta:
        model = models.Department


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name}.{o.last_name}@test.docplanner.com".lower()
    )
    department = factory.SubFactory(DepartmentFactory)
    country = factory.fuzzy.FuzzyChoice(enums.Countries)

    class Meta:
        model = models.User


class GoogleAuthServiceFactory(factory.Factory):
    class Meta:
        model = services.GoogleAuthService

    # Set your own default values for client ID, secret key, and redirect URL here
    GOOGLE_AUTH_CLIENT_ID = factory.fuzzy.FuzzyText(length=20)
    GOOGLE_AUTH_SECRET_KEY = factory.fuzzy.FuzzyText(length=40)
    GOOGLE_AUTH_REDIRECT_URL = "http://example.com/auth/google/callback"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Override _create() to return the instance directly
        return model_class()
