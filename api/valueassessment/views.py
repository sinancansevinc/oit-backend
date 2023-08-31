from datetime import datetime

from core import utils
from core.models import User
from core.views import DetailedModelViewSet
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import filters, models, serializers


class ValueViewSet(DetailedModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.ValueSerializer
    serializer_action_classes = {
        'retrieve': serializers.ValueRetrieveSerializer,
        'detailed': serializers.ValueDetailedSerializer,
    }
    filterset_class = filters.ValueFilter

    def create(self, request, *args, **kwargs):
        if not request.user.has_perm("values.add_value"):
            return Response({'error_message': 'You do not have permission to add value'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        isExist = models.Value.objects.filter(
            Q(role=data['role']) & Q(assignment_year=data['assignment_year'])).exists()

        if isExist:
            return Response({'error_message': 'Role and Year combination already exists'}, status=status.HTTP_400_BAD_REQUEST)

        data['created_by'] = request.user.id
        return super(ValueViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data

        created_at = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')


        if (created_at.year < datetime.now().year):
            return Response({'error_message': 'History data cannot be updated'}, status=status.HTTP_400_BAD_REQUEST)

        return super(ValueViewSet, self).update(request, *args, **kwargs)


class ValueAssessmentViewSet(DetailedModelViewSet):
    queryset = models.ValueAssessment.objects.all()
    serializer_class = serializers.ValueAssessmentSerializer
    serializer_action_classes = {
        'retrieve': serializers.ValueAssessmentRetrieveSerializer,
        'detailed': serializers.ValueAssessmentDetailedSerializer,
    }

    filterset_class = filters.ValueAssessmentFilter

    def update(self, request, *args, **kwargs):
        data = request.data
        data["updated_by"] = request.user.id
        value_assessment_items = data["value_assessment_items"]

        for value_assessment_item in value_assessment_items:
            if value_assessment_item["score"] > 9:
                return Response({'error_message': 'Score can not be greater than value proficiency'}, status=status.HTTP_400_BAD_REQUEST)

        return super(ValueAssessmentViewSet, self).update(request, *args, **kwargs)

    def get_queryset(self):
        value_queryset = self.queryset
        user = self.request.user

        if user.has_perm("valueassessment.view_valueassessment") and not user.has_perm("valueassessment.can_access_all_valueassessment"):
            value_queryset = self.queryset.filter(
                Q(target_employee=user))

        elif user.has_perm("valueassessment.can_access_all_valueassessment"):
            value_queryset = self.queryset
        else:
            return Response({"error_message": "You do not have permission to access value assessment"}, status=status.HTTP_401_UNAUTHORIZED)

        return value_queryset

    @action(
        detail=False,
        methods=['GET'],
    )
    def get_value_assessment_by_manager(self, request):
        user = request.user
        value_queryset = self.queryset.filter(assigned_employee=user)

        page = self.paginate_queryset(value_queryset)

        if page is not None:
            serializer = serializers.ValueAssessmentDetailedSerializer(
                page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data

        else:
            serializer = serializers.ValueAssessmentDetailedSerializer(
                value_queryset, many=True)
            data = serializer.data

        return Response(data)

    @action(detail=False, methods=['POST'])
    def add_peer_by_employee(self, request):

        user = User.objects.filter(
            email="sinancan.sevinc@docplanner.com").first()

        # user = request.user

        assigned_user = User.objects.filter(
            id=request.data['assigned_employee']).first()

        value_assessments_with_employee_peer = models.ValueAssessment.objects.filter(
            Q(target_employee=user) & Q(created_at__year=datetime.now().year) & Q(type="employee_peer"))

        # Maximum peer count is 4
        if (len(value_assessments_with_employee_peer) < 4):
            value_assessment = models.ValueAssessment.objects.filter(
                Q(target_employee=user) & Q(created_at__year=datetime.now().year)).first()

            new_value_assessment_by_peer = models.ValueAssessment(
                assigned_employee=assigned_user,
                target_employee=user,
                type="employee_peer",
                created_by=user

            )

            new_value_assessment_by_peer.save()

            value_assessment_items_for_peers = []

            for item in value_assessment.value_assessment_items.all():
                value_assessment_item_to_db = models.ValueAssessmentItem(
                    value_item=item.value_item,
                    score=0
                )
                value_assessment_items_for_peers.append(
                    value_assessment_item_to_db)

            models.ValueAssessmentItem.objects.bulk_create(
                value_assessment_items_for_peers)

            new_value_assessment_by_peer.value_assessment_items.set(
                value_assessment_items_for_peers)

            return Response(serializers.ValueAssessmentDetailedSerializer(new_value_assessment_by_peer).data)
        else:
            return Response({"error_message": "You can not add more than 4 peer to value assessment"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def add_peer_by_manager(self, request):

        created_user = User.objects.filter(id=request.user.id).first()

        request.user.id

        assigned_user = User.objects.filter(
            id=request.data['assigned_employee']).first()
        target_employee = User.objects.filter(
            id=request.data['target_employee']).first()

        if not target_employee.manager == request.user:
            return Response({"error_message": "You do not have permission to add peer to value assessment"}, status=status.HTTP_401_UNAUTHORIZED)

        value_assessments_with_manager_peer = models.ValueAssessment.objects.filter(
            Q(target_employee=target_employee) & Q(created_at__year=datetime.now().year) & Q(type="manager_peer"))

        # Maximum employee peer count is 4
        if (len(value_assessments_with_manager_peer) < 4):
            value_assessment = models.ValueAssessment.objects.filter(
                Q(target_employee=target_employee) & Q(created_at__year=datetime.now().year)).first()

            new_value_assessment_by_peer = models.ValueAssessment(
                assigned_employee=assigned_user,
                target_employee=target_employee,
                type="manager_peer",
                created_by=created_user

            )
            new_value_assessment_by_peer.save()

            value_assessment_items_for_peers = []

            for item in value_assessment.value_assessment_items.all():
                value_assessment_item_to_db = models.ValueAssessmentItem(
                    value_item=item.value_item,
                    score=0
                )
                value_assessment_items_for_peers.append(
                    value_assessment_item_to_db)

            models.ValueAssessmentItem.objects.bulk_create(
                value_assessment_items_for_peers)

            new_value_assessment_by_peer.value_assessment_items.set(
                value_assessment_items_for_peers)

            return Response(serializers.ValueAssessmentDetailedSerializer(new_value_assessment_by_peer).data)
        else:
            return Response({"error_message": "You can not add more than 4 peer to value assessment"}, status=status.HTTP_401_UNAUTHORIZED)
