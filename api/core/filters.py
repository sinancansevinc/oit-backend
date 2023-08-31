from core import models
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        label=_("first name"), lookup_expr="icontains")
    last_name = filters.CharFilter(
        label=_("last name"), lookup_expr="icontains")
    full_name = filters.CharFilter(
        method="filter_full_name",
        label=_("full name"),
    )
    department = filters.CharFilter(
        method="filter_department",
        label=_("department"),
    )

    class Meta:
        model = models.User
        fields = (
            "is_active",
            "country"
        )

    def filter_full_name(self, qs, name, value):
        qs = qs.annotate(
            full_name=Concat("first_name", Value(" "), "last_name")
        ).filter(full_name__icontains=value)
        return qs

    def filter_department(self, qs, name, value):
        qs = qs.filter(
            Q(department_id=value)
            | Q(department__parent_id=value)
            | Q(department__parent__parent_id=value)
        )
        return qs
