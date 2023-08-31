from core import filters, models, serializers, services
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from goal.models import Goal
from goal.serializers import GoalDetailedSerializer
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from valueassessment.models import ValueAssessment
from valueassessment.serializers import ValueAssessmentSerializer


class DetailedViewSetMixin:
    _manager_method_prefix = "action_"
    serializer_action_classes = {}
    ordering = ("id",)

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            queryset = getattr(
                queryset, f"{self._manager_method_prefix}{self.action}"
            )().all()
        except (AttributeError,):
            pass
        return queryset

    @action(detail=False)
    def detailed(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        kwargs.update({"many": True, "context": {"request": self.request}})
        if page is not None:
            serializer = self.get_serializer_class()(page, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer_class()(queryset, **kwargs)
        return Response(serializer.data)


class DetailedModelViewSet(DetailedViewSetMixin, viewsets.ModelViewSet):
    pass


class RetrieveModelViewSet(
    DetailedViewSetMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class UserModelViewSet(DetailedModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_class = filters.UserFilter
    serializer_action_classes = {
        "retrieve": serializers.UserRetrieveSerializer,
        "detailed": serializers.UserDetailedListSerializer,
        "profile": serializers.UserProfileSerializer,
    }
    order_fields = (
        "id",
        "is_active",
    )

    @action(detail=False)
    def permissions(self, request, *args, **kwargs):
        """
        Return permissions for current user.
        """
        return Response(request.user.get_all_permissions())

    @action(detail=False)
    def profile(self, request, *args, **kwargs):
        """
        Return user profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False)
    def get_users_under_manager(self, request, *args, **kwargs):
        user_manager = request.user

        if user_manager.has_perm("core.can_access_all_users"):
            qs = models.User.objects.filter(
                is_active=True).order_by("first_name")
        else:
            qs = models.User.objects.all().filter(is_active=True).filter(
                Q(manager=user_manager) |
                Q(manager__manager=user_manager) |
                Q(manager__manager__manager=user_manager) |
                Q(manager__manager__manager__manager=user_manager)
            ).order_by("first_name")

        serializer = serializers.UserProfileSerializer(
            qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def get_score(self, request, *args, **kwargs):
        goal_score = 0
        value_assessment_score = 0

        test_user = models.User.objects.filter(id=2).first()
        # user = request.user

        # Goal Scores Calculated
        goals = Goal.objects.filter(Q(assignment_year=timezone.now().year) & Q(
            target_employee=test_user)).all()

        goal_serializer = GoalDetailedSerializer(goals, many=True)

        goal_score = sum(item["score"] for item in goal_serializer.data)

        # Value Assessment Scores Calculated
        value_assessments = ValueAssessment.objects.filter(Q(created_at__year=timezone.now().year) & Q(
            target_employee=test_user)).all()

        value_assessment_serializer = ValueAssessmentSerializer(
            value_assessments, many=True)

        value_assessment_score = sum(
            assessment["score"] for assessment in value_assessment_serializer.data)

        if len(goal_serializer.data) == 0:
            goal_avg = 0
        else:
            goal_avg = round(goal_score / len(goal_serializer.data), 2)

        if len(value_assessment_serializer.data) == 0:
            value_assessment_avg = 0
        else:
            value_assessment_avg = round(
                value_assessment_score / len(value_assessment_serializer.data), 2)

        response = {
            "total_goal_score": goal_avg,
            "total_value_assessment_score": value_assessment_avg
        }

        return Response(response, 200)


class DepartmentViewSet(DetailedModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [IsAuthenticated]
    serializer_action_classes = {
        "retrieve": serializers.DepartmentRetrieveSerializer,
        "detailed": serializers.DepartmentDetailedListSerializer,
    }
    order_fields = (
        "id",
        "name",
    )
    ordering = ("id",)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        from django.contrib.auth import logout
        logout(request)
        return Response(status=status.HTTP_200_OK)


class GoogleAuthView(APIView):
    serializer_class = serializers.GoogleAuthSerializer

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data["code"]

        if not code:
            raise ValidationError({
                "message": "Please provide the auth code."
            })

        service = services.GoogleAuthService()

        access_token = service.get_access_token(code)
        profile_info = service.get_profile_info(access_token)

        if access_token is None or profile_info is None:
            raise ValidationError({
                "message": "Access token or profile info is not valid"
            })

        user_email = profile_info["email"]

        if not user_email.endswith("@docplanner.com"):
            raise ValidationError({
                "message": "Please use docplanner account."
            })

        first_name = profile_info["given_name"]
        last_name = profile_info["family_name"]
        email_split = user_email.split("@")
        username = email_split[0]

        user = models.User.objects.filter(email=user_email).first()
        if not user:
            models.User.objects.create_user(
                email=user_email, first_name=first_name, last_name=last_name, username=username)

        user = models.User.objects.get(email=user_email)
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save()

        login_user = authenticate(username=username, password=user.password)
        if login_user is not None:
            login(request, user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "department": user.department.name if user.department else None,
                },
                "permissions": user.get_all_permissions(),
            }
        )
