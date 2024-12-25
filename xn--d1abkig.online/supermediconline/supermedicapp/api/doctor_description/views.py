from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import supermedicapp.models as models
import supermedicapp.api.doctor_description.serializers as serializers


class DoctorDescriptionView(APIView):
    def get(self, request):
        doctor_description_id = request.GET.get("id")
        try:
            doctor = models.DoctorDescription.objects.filter(
                pk=doctor_description_id
            ).first()
            serializer = serializers.DoctorGetSerializer(doctor)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
