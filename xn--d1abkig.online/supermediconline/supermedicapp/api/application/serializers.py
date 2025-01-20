from rest_framework import serializers
import supermedicapp.models as models


class ApplicationErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Error message details.")


class ApplicationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = (
            "id",
            "is_paid",
            "created_at",
            "link_sent",
            "is_notified",
            "appointment_id",
            "is_deleted",
        )


class ApplicationUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    appointment_id = serializers.IntegerField(required=False)
    is_paid = serializers.BooleanField(required=False)
    is_notified = serializers.BooleanField(required=False)
    link_sent = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
