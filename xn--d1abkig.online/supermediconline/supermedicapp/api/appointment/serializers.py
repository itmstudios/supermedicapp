from rest_framework import serializers
import supermedicapp.models as models


class AppointmentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = (
            "id",
            "appointment_time",
            "is_notified",
            "is_deleted",
            "doctor_specialization_id",
            "patient_id",
        )


class AppointmentUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    patient_id = serializers.IntegerField(required=False)
    is_notified = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
