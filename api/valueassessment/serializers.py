from core.enums import GenericStatuses
from core.serializers import KeyValueChoiceField, UserDetailedListSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from . import enums, models


class ValueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ValueItem
        fields = "__all__"


class ValueSerializer(WritableNestedModelSerializer):
    value_items = ValueItemSerializer(many=True)

    class Meta:
        model = models.Value
        fields = "__all__"


class ValueRetrieveSerializer(ValueSerializer):
    created_by = UserDetailedListSerializer()
    role = KeyValueChoiceField(choices=enums.ValueRoles)


class ValueDetailedSerializer(ValueRetrieveSerializer):
    pass


class ValueAssessmentItemSerializer(serializers.ModelSerializer):
    value_item = ValueItemSerializer(read_only=True)

    class Meta:
        model = models.ValueAssessmentItem
        fields = '__all__'


class ValueAssessmentSerializer(WritableNestedModelSerializer):
    value_assessment_items = ValueAssessmentItemSerializer(many=True)
    score = serializers.SerializerMethodField()

    def get_score(self, obj, *args, **kwargs):
        value_assessment_items = obj.value_assessment_items.all()
        total_score = 0
        total_proficiency = 0
        
        for i in value_assessment_items:
            total_score += i.score
            total_proficiency += i.value_item.proficiency

        if total_proficiency == 0:
            return 0

        return round((total_score / total_proficiency * 100),2)

    class Meta:
        model = models.ValueAssessment
        fields = '__all__'


class ValueAssessmentRetrieveSerializer(ValueAssessmentSerializer):
    target_employee = UserDetailedListSerializer()
    assigned_employee = UserDetailedListSerializer()
    status = KeyValueChoiceField(choices=GenericStatuses)
    type = KeyValueChoiceField(choices=enums.ValueAssessmentTypes)



class ValueAssessmentDetailedSerializer(ValueAssessmentRetrieveSerializer):
    pass
