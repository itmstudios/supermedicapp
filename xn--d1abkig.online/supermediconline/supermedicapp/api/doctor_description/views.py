import supermedicapp.api.doctor_description.serializers as serializers
import supermedicapp.models as models
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DoctorDescriptionView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='doctor_description_id', required=False, type=int),
        ],
        responses={
            200: serializers.DoctorGetSerializer,
            400: OpenApiResponse(
                description="Error message",
                response=serializers.DoctorErrorResponseSerializer,
            )
        },
    )
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
