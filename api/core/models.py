from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField, CICharField
from django.core.validators import MinLengthValidator
from django.db import models

from . import enums, managers

# Create your models here.


class Department(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               limit_choices_to=models.Q(parent__isnull=True)
                               | models.Q(parent__parent__isnull=True))

    name = models.CharField(max_length=100)

    objects = managers.DepartmentManager.as_manager()

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent} - {self.name}"
        return self.name

    class Meta:
        verbose_name = "department"
        verbose_name_plural = "departments"
        indexes = [
            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_department_name"
            )
        ]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, null=True, blank=True)
    docplanner_id = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(
        max_length=100, validators=(MinLengthValidator(1),))
    last_name = models.CharField(
        max_length=100, validators=(MinLengthValidator(1),))
    email = models.EmailField(unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, null=True, blank=True)

    country = models.CharField(
        choices=enums.Countries.choices, max_length=15, null=True, blank=True)

    manager = models.ForeignKey(
        "User", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(null=True, blank=True)
    termination_date = models.DateTimeField(null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    objects = managers.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
            models.Index(fields=["email"]),
            models.Index(fields=["is_active"]),
        ]

        permissions = (
            (
                "can_access_all_users",
                "can access all users"
            ),
        )

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip().title()

    def get_short_name(self) -> str:
        return self.first_name

    def has_any_perms(self, perm_list, obj=None):
        """
        Return True if the user has any of the specified permissions. If
        object is passed, check if the user has any required perms for it.
        """
        return any(self.has_perm(perm, obj) for perm in perm_list)

    def __str__(self) -> str:
        return self.get_full_name()

    @property
    def is_staff(self) -> bool:
        """
        This property supply is_staff parameter to make sure admin panel works.
        """
        return True
