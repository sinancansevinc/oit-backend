import json

from core.factories import UserFactory
from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status
# Create your tests here.
from rest_framework.test import APIRequestFactory

from . import factories, models, serializers, views


class ValueItemModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.ValueItemFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.name)


class ValueModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.ValueFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.name)


class ValueAssessmentItemModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.ValueAssessmentItemFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.value_item.name)


class ValueAssessmentModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.ValueAssessmentFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.value.name)


class ValueSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.ValueFactory()

    def test_list_serializer_query_count(self):
        factories.ValueFactory()
        with self.assertNumQueries(3):
            serializers.ValueSerializer(
                models.Value.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(3):
            serializers.ValueRetrieveSerializer(
                models.Value.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.ValueFactory()
        with self.assertNumQueries(4):
            serializers.ValueDetailedSerializer(
                models.Value.objects.action_detailed().all(), many=True
            ).data


class ValueItemSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.ValueItemFactory()

    def test_list_serializer_query_count(self):
        factories.ValueItemFactory()
        with self.assertNumQueries(1):
            serializers.ValueItemSerializer(
                models.ValueItem.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(1):
            serializers.ValueItemSerializer(
                models.ValueItem.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.ValueItemFactory()
        with self.assertNumQueries(1):
            serializers.ValueItemSerializer(
                models.ValueItem.objects.action_detailed().all(), many=True
            ).data


class ValueAssessmentItemSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.ValueAssessmentItemFactory()

    def test_list_serializer_query_count(self):
        factories.ValueAssessmentItemFactory()
        with self.assertNumQueries(3):
            serializers.ValueAssessmentItemSerializer(
                models.ValueAssessmentItem.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(1):
            serializers.ValueAssessmentItemSerializer(
                models.ValueAssessmentItem.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.ValueAssessmentItemFactory()
        with self.assertNumQueries(1):
            serializers.ValueAssessmentItemSerializer(
                models.ValueAssessmentItem.objects.action_detailed().all(), many=True
            ).data


class ValueAssessmentSerializerTestCase(TestCase):
    def setUp(self):
        self.obj = factories.ValueAssessmentFactory()

    def test_list_serializer_query_count(self):
        factories.ValueAssessmentFactory()
        with self.assertNumQueries(9):
            serializers.ValueAssessmentSerializer(
                models.ValueAssessment.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(3):
            serializers.ValueAssessmentSerializer(
                models.ValueAssessment.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.ValueAssessmentFactory()
        with self.assertNumQueries(5):
            serializers.ValueAssessmentSerializer(
                models.ValueAssessment.objects.action_detailed().all(), many=True
            ).data


class ValueViewTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.ValueFactory()
        self.factory = APIRequestFactory()
        self.url = f"value/"
        self.view = views.ValueViewSet.as_view(
            {"post": "create"})
        self.request = self.factory.post(
            self.url,
            json.dumps({"name": "Value", "year": "2023-7-30",
                       "role": "manager", "created_by": "1", "value_items": ""}),
            content_type="application/json",
        )

    def test_value_without_permission(self):
        response = self.view(self.request).render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_value_with_permission(self):
        created_by = UserFactory()
        perms = Permission.objects.filter(
            codename__in=(["add_value", "view_value"]),
            content_type__app_label="valueassessment",
        ).all()
        created_by.user_permissions.set(perms)
        self.request.user = created_by


class ValueAssessmentViewTestCase(TestCase):

    def setUp(self) -> None:
        self.obj = factories.ValueAssessmentFactory()
        self.factory = APIRequestFactory()
        self.url = f'valueassessment/'
        self.view = views.ValueAssessmentViewSet.as_view({'get': 'list'})
        self.request = self.factory.get(self.url)

    def test_value_assessment_without_permission(self):
        response = self.view(self.request).render()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_value_assessment_with_permission(self):
        created_by = UserFactory()
        perms = Permission.objects.filter(codename__in=(
            ['add_valueassessment', 'view_valueassessment']), content_type__app_label='valueassessment').all()
        created_by.user_permissions.set(perms)
        self.request.user = created_by
        response = self.view(self.request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
