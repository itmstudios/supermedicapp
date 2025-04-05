from rest_framework import serializers
import supermedicapp.models as models


class UserErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Error message details.")


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "telegram_id",
            "telegram_username",
            "phone_number",
        )
