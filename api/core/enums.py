from django.db import models


class Countries(models.TextChoices):
    POLAND = "pl"
    GERMANY = "de"
    SPAIN = "es"
    ITALY = "it"
    BRAZIL = "br"
    MEXICO = "mx"
    TURKEY = "tr"
    COLOMBIA = "co"


class GenericStatuses(models.TextChoices):
    CREATED = "created"
    APPROVED = "approved"
