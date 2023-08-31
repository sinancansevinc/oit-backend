from datetime import datetime

from core import utils
from core.models import User
from django.db.models import Q
from django.utils import timezone
from oit_backend.celery import app

from . import models, serializers


@app.task()
def assign_value_assessments() -> None:
    current_year = datetime.now().year
    users = User.objects.all()
    individual_value = models.Value.objects.filter(
        Q(role="individual") &
        Q(assignment_year=current_year)
    )
    manager_value = models.Value.objects.filter(
        Q(role="manager") &
        Q(assignment_year=current_year)
    )

    if not individual_value.exists():
        return "There is no individual value for {current_year}."

    if not manager_value.exists():
        return "There is no individual value for {current_year}."

    # Assign value assessment form to the users
    for user in users:
        is_manager = utils.is_manager(user)
        value_items = []
        if is_manager:
            value_items = manager_value.first().value_items.all()
        else:
            value_items = individual_value.first().value_items.all()

        self_value_assessment = models.ValueAssessment.objects.filter(
            target_employee=user).filter(Q(type="employee") & Q(created_at__year=current_year))
        manager_value_assessment = models.ValueAssessment.objects.filter(
            target_employee=user).filter(Q(type="manager") & Q(created_at__year=current_year))

        # Create individual assessment
        if not self_value_assessment.exists():

            # Prepare value asssessment items
            value_items_to_db = [models.ValueAssessmentItem(
                value_item=item, score=0) for item in value_items]
            models.ValueAssessmentItem.objects.bulk_create(value_items_to_db)

            value_assessment_by_employee = models.ValueAssessment(
                target_employee=user,
                assigned_employee=user,
                type="employee",
            )
            value_assessment_by_employee.save()

            for assessment_item in value_items_to_db:
                value_assessment_by_employee.value_assessment_items.add(
                    assessment_item)

        # Create manager assessment
        if user.manager and not manager_value_assessment.exists():
            # Prepare value asssessment items
            value_items_to_db = [models.ValueAssessmentItem(
                value_item=item, score=0) for item in value_items]
            models.ValueAssessmentItem.objects.bulk_create(value_items_to_db)

            value_assessment_by_manager = models.ValueAssessment(
                target_employee=user,
                assigned_employee=user.manager,
                type="manager",
            )
            value_assessment_by_manager.save()

            for assessment_item in value_items_to_db:
                value_assessment_by_manager.value_assessment_items.add(
                    assessment_item)
