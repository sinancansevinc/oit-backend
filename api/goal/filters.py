from core.enums import GenericStatuses
from django_filters import rest_framework as filters

from . import enums, models


class GoalFilter(filters.FilterSet):

    employee_name = filters.CharFilter(
        field_name="target_employee__first_name",
        lookup_expr="icontains",
        label="Employee"
    )

    department_name = filters.CharFilter(
        field_name="target_employee__department__name",
        lookup_expr="icontains",
        label="Department"
    )

    status = filters.MultipleChoiceFilter(
        field_name="status",
        label="Status",
        choices=GenericStatuses.choices
    )

    quarter = filters.MultipleChoiceFilter(
        field_name="quarter",
        label="Quarter",
        choices=enums.Quarters.choices
    )

    assignment_year = filters.NumberFilter(
        field_name="assignment_year",
        label="Year"
    )

    class Meta:
        model = models.Goal
        fields = ['target_employee', 'status', 'quarter', 'assignment_year']

    def filter_year(self, qs, name, value):
        return qs.filter(assignment_year=value)
