from rest_framework import serializers
import supermedicapp.models as models


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
