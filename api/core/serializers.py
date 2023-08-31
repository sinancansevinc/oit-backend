from core import models
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class KeyValueChoiceField(serializers.ChoiceField):
    """
    The choices field data has been represented as a key-value. For example;

    class Choice(Enum):
        MALE = "m", "Male"
        FEMALE = "f", "Female"

    {"key": "m", "value": "Male"}
    """

    def to_representation(self, value):
        key = super().to_representation(value=value)
        if key:
            return {"value": key.value, "display_name": key.label}
        return {"value": "", "display_name": ""}


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data


class DepartmentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Department.objects.all(), required=False
    )
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=models.Department.objects.all())]
    )

    class Meta:
        model = models.Department
        fields = "__all__"
        
class DepartmentRetrieveSerializer(DepartmentSerializer):
    parent = RecursiveField(read_only=True)

class DepartmentDetailedListSerializer(DepartmentRetrieveSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(
        method_name="get_full_name", label=_("full name")
    )

    class Meta:
        model = models.User
        fields = (
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "department",
            "is_active",
        )

    def get_full_name(self, obj):
        return obj.get_full_name()
    
class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentRetrieveSerializer(read_only=True)
    full_name = serializers.SerializerMethodField(
        method_name="get_full_name", label=_("full name")
    )

    class Meta:
        model = models.User
        fields = ("id","first_name", "last_name","full_name","email", "department")

    
    def get_full_name(self, obj):
        return obj.get_full_name()

class UserRetrieveSerializer(UserSerializer):
    department = DepartmentRetrieveSerializer(read_only=True)
class UserDetailedListSerializer(UserRetrieveSerializer):
    pass

class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField()
