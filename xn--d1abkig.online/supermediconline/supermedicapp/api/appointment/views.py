import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import supermedicapp.models as models
import supermedicapp.api.appointment.serializers as serializers

logger = logging.getLogger(__name__)


class AppointmentView(APIView):
    def get(self, request):
        appointment_id = request.GET.get("appointment_id")
        patient_id = request.GET.get("patient_id")
        is_notified = request.GET.get("is_notified")
        is_deleted = request.GET.get("is_deleted")
        try:
            if str(patient_id) == "1":
                appointment = models.Appointment.objects.filter(
                    patient__isnull=False,
                    is_notified=is_notified,
                    is_deleted=is_deleted,
                )
                serializer = serializers.AppointmentGetSerializer(
                    appointment, many=True
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            if is_notified is not None and is_deleted is not None:
                appointment = models.Appointment.objects.filter(
                    is_notified=is_notified,
                    is_deleted=is_deleted,
                )
                serializer = serializers.AppointmentGetSerializer(
                    appointment, many=True
                )
            else:
                appointment = models.Appointment.objects.filter(
                    pk=appointment_id
                ).first()
                serializer = serializers.AppointmentGetSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        serializer = serializers.AppointmentUpdateSerializer(data=request.data)
        if serializer.is_valid():
            appointment_id = serializer.validated_data.get("id")
            patient_id = serializer.validated_data.get("patient_id")
            is_notified = serializer.validated_data.get("is_notified")
            is_deleted = serializer.validated_data.get("is_deleted")
            try:
                appointment = models.Appointment.objects.get(pk=appointment_id)
            except Exception as e:
                logger.error(f'unable to find appointment {appointment_id}', e)
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                if str(patient_id) == "0":
                    appointment.patient_id = None
                if is_notified is not None:
                    appointment.is_notified = is_notified
                if is_deleted is not None:
                    appointment.is_deleted = is_deleted

                appointment.save()
                return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
