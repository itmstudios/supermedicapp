from rest_framework import serializers
import supermedicapp.models as models


class DoctorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorDescription
        fields = ("id", "doctor_id", "consultation_price")
