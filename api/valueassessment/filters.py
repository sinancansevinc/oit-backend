from datetime import datetime

from core.enums import GenericStatuses
from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from . import enums, models


class ValueFilter(filters.FilterSet):

    role = filters.MultipleChoiceFilter(
        field_name="role",
        label="Role",
        choices=enums.ValueRoles.choices
    )
    
    year = filters.NumberFilter(
        field_name="assignment_year",
        label="Year"
    )
    

    class Meta:
        model = models.Value
        fields = ['created_at']
        
    def filter_year(self, qs, name, value):
        return qs.filter(assignment_year=value)



class ValueAssessmentFilter(filters.FilterSet):
    status = filters.MultipleChoiceFilter(
        field_name="status",
        label="Status",
        choices=GenericStatuses.choices
    )

    target_employee_name = filters.CharFilter(
        field_name="target_employee__first_name",
        lookup_expr="icontains",
        label=" Target employee name",
    )

    assigned_employee_name = filters.CharFilter(
        field_name="assigned_employee__first_name",
        lookup_expr="icontains",
        label="Assigned employee name",
    )

    type = filters.MultipleChoiceFilter(
        field_name="type",
        label="Type",
        choices=enums.ValueAssessmentTypes.choices
    )

    class Meta:
        model = models.ValueAssessment
        fields = ['target_employee', 'assigned_employee', 'status', 'type']
