from core.models import User
from core.views import DetailedModelViewSet
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import filters, models, serializers


class GoalViewSet(DetailedModelViewSet):
    queryset = models.Goal.objects.all()
    serializer_class = serializers.GoalSerializer
    serializer_action_classes = {
        'retrieve': serializers.GoalRetrieveSerializer,
        'detailed': serializers.GoalDetailedSerializer,
    }
    filterset_class = filters.GoalFilter

    def get_queryset(self):
        user = self.request.user

        if user.has_perm("goal.view_goal") and not user.has_perm(
            "goal.can_access_all_goal"
        ):
            oit_query = self.queryset.filter(
                Q(target_employee=user)
            )

        elif user.has_perm("goal.can_access_all_goal"):
            oit_query = self.queryset
        else:
            return Response({"error_message": "You do not have permission to access Goal"}, status=status.HTTP_401_UNAUTHORIZED)

        return oit_query

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        assigned_user = models.User.objects.filter(
            id=request.data['target_employee']).first()

        isExist = models.Goal.objects.filter(
            Q(assignment_year=request.data['assignment_year']) & Q(target_employee=assigned_user) & Q(quarter=request.data['quarter'])).exists()

        if isExist:
            return Response({'error_message': 'Goal is already assigned to employee.'}, status=status.HTTP_400_BAD_REQUEST)

        return super(GoalViewSet, self).create(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["GET"],
    )
    def get_goals_by_manager(self, request, *args, **kwargs):

        user = request.user
        goal_queryset = models.Goal.objects.filter(
            Q(target_employee__manager=user)
            | Q(target_employee__manager__manager=user)
            | Q(target_employee__manager__manager__manager=user)
            | Q(target_employee__manager__manager__manager__manager=user)).all()

        page = self.paginate_queryset(goal_queryset)

        if page is not None:
            serializer = serializers.GoalDetailedSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
            # return self.get_paginated_response(serializer.data)

        else:
            serializer = serializers.GoalDetailedSerializer(
                goal_queryset, many=True)
            data = serializer.data

        return Response(data)


# TODO LATER
# class FeedbackViewSet(DetailedModelViewSet):
#     queryset = models.Feedback.objects.all()
#     serializer_class = serializers.FeedbackSerializer
#     serializer_action_classes = {
#         'retrieve': serializers.FeedbackRetrieveSerializer,
#         'detailed': serializers.FeedbackRetrieveSerializer,
#     }

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         print(request.user)
#         request.data['created_by'] = request.user.id
#         return super(FeedbackViewSet, self).create(request, *args, **kwargs)
