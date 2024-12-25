from rest_framework import serializers
import supermedicapp.models as models


class UserStepGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserStep
        fields = (
            "id",
            "name",
            "telegram_username",
            "telegram_id",
            "select_specialization_step",
            "select_doctor_step",
            "select_date_step",
            "select_time_step",
            "user_info_step",
            "created_at",
        )


class UserStepUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    is_notified = serializers.BooleanField(required=True)
