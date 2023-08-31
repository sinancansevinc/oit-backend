from django.db import models


class ValueRoles(models.TextChoices):
    INDIVIDUAL = "individual"
    MANAGER = "manager"


class ValueAssessmentTypes(models.TextChoices):
    MANAGER = "manager"
    EMPLOYEE = "employee"
    MANAGER_PEER = "manager_peer"
    EMPLOYEE_PEER = "employee_peer"
