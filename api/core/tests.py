from unittest.mock import Mock, patch

from django.test import TestCase

from . import factories, models, serializers


class DepartmentModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.DepartmentFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.name)

# Create your tests here.


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.UserFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), str(self.obj.get_full_name()))


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.UserFactory()

    def test_list_serializer_query_count(self):
        factories.UserFactory()
        with self.assertNumQueries(1):
            serializers.UserDetailedListSerializer(
                models.User.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(1):
            serializers.UserRetrieveSerializer(
                models.User.objects.action_retrieve().first()
            ).data

    def test_list_serializer_query_count(self):
        factories.UserFactory()
        with self.assertNumQueries(1):
            serializers.UserDetailedListSerializer(
                models.User.objects.action_detailed().all(), many=True
            ).data


class DepartmentSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.DepartmentFactory()

    def test_list_serializer_query_count(self):
        factories.DepartmentFactory()
        with self.assertNumQueries(1):
            serializers.DepartmentSerializer(
                models.Department.objects.action_list(), many=True
            ).data


class GoogleAuthServiceTestCase(TestCase):

    def setUp(self):
        self.google_auth = factories.GoogleAuthServiceFactory()
        

    @patch('core.services.GoogleAuthService')
    def test_get_access_token_failure(self, mock_post=None):

        if mock_post is None:
            mock_post = Mock()
            mock_post.return_value.status_code = 401
            mock_post.return_value.json.return_value = {
                "error": "invalid_grant"}

        access_token = self.google_auth.get_access_token("invalid_code")

        self.assertIsNone(access_token)

    def test_get_profile_info_failure(self, mock_get=None):
        
        if mock_get is None:
            mock_get = Mock()
            mock_get.return_value.status_code = 401
            mock_get.return_value.json.return_value = {"error": "invalid_token"}

        profile_info = self.google_auth.get_profile_info(
            "invalid_access_token")

        self.assertIsNone(profile_info)
