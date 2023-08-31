from core.serializers import UserDetailedListSerializer
from django.shortcuts import get_object_or_404
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from core.enums import GenericStatuses
from core.serializers import KeyValueChoiceField

from . import enums, models


class MoonshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Moonshot
        fields = '__all__'


class HandshakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Handshake
        fields = '__all__'


class GoalSerializer(WritableNestedModelSerializer):
    moonshots = MoonshotSerializer(many=True)
    handshakes = HandshakeSerializer(many=True)

    class Meta:
        model = models.Goal
        fields = '__all__'


class GoalRetrieveSerializer(GoalSerializer):
    created_by = UserDetailedListSerializer()
    status = KeyValueChoiceField(choices=GenericStatuses)
    target_employee = UserDetailedListSerializer()
    score = serializers.SerializerMethodField()
    quarter = KeyValueChoiceField(choices=enums.Quarters)

    def get_score(self, obj, *args, **kwargs):
        handshakes = obj.handshakes.all()
        completed_handshakes = handshakes.filter(is_succeed=True)
        if len(handshakes) == 0:
            return 0
        return round(len(completed_handshakes) / len(handshakes) * 100,2)


class GoalDetailedSerializer(GoalRetrieveSerializer):
    pass


#TODO LATER
# class FeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Feedback
#         fields = '__all__'


# class FeedbackRetrieveSerializer(FeedbackSerializer):
#     created_by = UserDetailedListSerializer()
#     target_employee = UserDetailedListSerializer()
