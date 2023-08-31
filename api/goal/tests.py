from django.test import TestCase

from . import enums, factories, models, serializers

# Create your tests here.


class MoonshootModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.MoonshotFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.name)


class HandshakeModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.HandshakeFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.name)


class GoalModelTestCase(TestCase):
    def setUp(self):
        self.obj = factories.GoalFactory()

    def test_string_representation(self):
        self.assertEqual(str(self.obj), self.obj.title)


class MoonshotSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.MoonshotFactory()

    def test_list_serializer_query_count(self):
        factories.MoonshotFactory()
        with self.assertNumQueries(1):
            serializers.MoonshotSerializer(
                models.Moonshot.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(1):
            serializers.MoonshotSerializer(
                models.Moonshot.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.MoonshotFactory()
        with self.assertNumQueries(1):
            serializers.MoonshotSerializer(
                models.Moonshot.objects.action_detailed().all(), many=True
            ).data


class HandshakeSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.HandshakeFactory()

    def test_list_serializer_query_count(self):
        factories.HandshakeFactory()
        with self.assertNumQueries(1):
            serializers.HandshakeSerializer(
                models.Handshake.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(1):
            serializers.HandshakeSerializer(
                models.Handshake.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.HandshakeFactory()
        with self.assertNumQueries(1):
            serializers.HandshakeSerializer(
                models.Handshake.objects.action_detailed().all(), many=True
            ).data


class GoalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.obj = factories.GoalFactory()

    def test_list_serializer_query_count(self):
        factories.GoalFactory()
        with self.assertNumQueries(5):
            serializers.GoalSerializer(
                models.Goal.objects.action_list().all(), many=True
            ).data

    def test_retrieve_serializer_query_count(self):
        with self.assertNumQueries(5):
            serializers.GoalRetrieveSerializer(
                models.Goal.objects.action_retrieve().first()
            ).data

    def test_detailed_serializer_query_count(self):
        factories.GoalFactory()
        with self.assertNumQueries(7):
            serializers.GoalDetailedSerializer(
                models.Goal.objects.action_detailed().all(), many=True
            ).data
