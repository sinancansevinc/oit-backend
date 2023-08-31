from datetime import datetime

from core.enums import GenericStatuses
from core.models import User
from django.core import validators
from django.db import models
from django.utils import timezone

from . import enums, managers


# Create your models here.
class ValueItem(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True, max_length=1000)

    objects = managers.ValueItemManager.as_manager()

    def __str__(self):
        return self.name


class Value(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50, choices=enums.ValueRoles.choices, default=enums.ValueRoles.INDIVIDUAL)
    assignment_year = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(2023),
            validators.MaxValueValidator(2100),
        ),
        default=timezone.now().year,
    )

    value_items = models.ManyToManyField(ValueItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="value_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="value_update_by")

    objects = managers.ValueManager.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment_year", "role"],
                name="unique_role_year",
            )
        ]

        permissions = (
            ("can_access_all_value", "can access all value"),
        )

    def __str__(self):
        return self.name


class ValueAssessmentItem(models.Model):
    value_item = models.ForeignKey(ValueItem, on_delete=models.PROTECT)
    score = models.PositiveBigIntegerField()

    objects = managers.ValueAssessmentItemManager.as_manager()

    def __str__(self):
        return self.value_item.name


class ValueAssessment(models.Model):
    target_employee = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="valueassessment_target_employee")
    assigned_employee = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="valueassessment_assigned_employee")
    status = models.CharField(
        max_length=10, choices=GenericStatuses.choices, default=GenericStatuses.CREATED)
    value_assessment_items = models.ManyToManyField(ValueAssessmentItem)
    type = models.CharField(max_length=50, choices=enums.ValueAssessmentTypes.choices,
                            default=enums.ValueAssessmentTypes.MANAGER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="valueassessment_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="valueassessment_updated_by")

    objects = managers.ValueAssessmentManager.as_manager()

    class Meta:
        constraints = []

        permissions = (
            ("can_access_all_valueassessment", "can access all value assessment"),
        )

    def __str__(self):
        return self.target_employee.username
