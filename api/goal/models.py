from core.enums import GenericStatuses
from core.models import User
from django.core import validators
from django.db import models
from django.utils import timezone

from . import enums, managers

# Create your models here.


class Handshake(models.Model):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=100, blank=True, null=True)
    is_succeed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    objects = managers.HandshakeManager.as_manager()


class Moonshot(models.Model):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=100, blank=True, null=True)
    is_succeed = models.BooleanField(default=False)

    objects = managers.MoonshotManager.as_manager()

    def __str__(self):
        return self.name


class Goal(models.Model):
    target_employee = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="goal_target_employee")
    quarter = models.CharField(max_length=10, choices=enums.Quarters.choices)

    assignment_year = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(2023),
            validators.MaxValueValidator(2100)
        ), default=timezone.now().year)

    moonshots = models.ManyToManyField(Moonshot)

    handshakes = models.ManyToManyField(Handshake)
    status = models.CharField(
        max_length=10, choices=GenericStatuses.choices, default=GenericStatuses.CREATED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="goal_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="goal_updated_by")

    objects = managers.GoalManager.as_manager()

    def __str__(self):
        return self.target_employee.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assignment_year', 'quarter', 'target_employee'], name='unique_oit_year_quarter')
        ]

        permissions = (
            ("can_access_all_goal", "can access all goal"),
        )

# TODO LATER
# class Feedback(models.Model):
#     target_employee = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name="feedback_target_employee")
#     created_by = models.ForeignKey(
#         User, on_delete=models.PROTECT, related_name="feedback_created_by")
#     comment = models.TextField(null=False, blank=False, max_length=1000)

#     def __str__(self):
#         return self.title
