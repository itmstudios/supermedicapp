from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import supermedicapp.models as models
import supermedicapp.api.application.serializers as serializers


class ApplicationView(APIView):
    def get(self, request):
        id = request.GET.get("id")
        appointment_id = request.GET.get("appointment_id")
        is_paid = request.GET.get("is_paid")
        is_notified = request.GET.get("is_notified")
        is_deleted = request.GET.get("is_deleted")
        if appointment_id is not None:
            try:
                applications = models.Application.objects.filter(
                    appointment_id=appointment_id,
                    is_paid=is_paid,
                    is_deleted=is_deleted,
                )
                serializer = serializers.ApplicationGetSerializer(
                    applications
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if is_paid is not None and is_notified is not None and is_deleted is not None:
            try:
                applications = models.Application.objects.filter(
                    is_paid=is_paid,
                    is_notified=is_notified,
                    is_deleted=is_deleted,
                )
                serializer = serializers.ApplicationGetSerializer(
                    applications, many=True
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                application = models.Application.objects.filter(pk=id).first()
                serializer = serializers.ApplicationGetSerializer(application)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = serializers.ApplicationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            is_paid = serializer.validated_data.get("is_paid")
            is_notified = serializer.validated_data.get("is_notified")
            link_sent = serializer.validated_data.get("link_sent")
            is_deleted = serializer.validated_data.get("is_deleted")
            application = []
            if request.data.get("id") is not None:
                application = models.Application.objects.get(pk=request.data.get("id"))
            if request.data.get("appointment_id") is not None:
                application = models.Application.objects.get(
                    appointment_id=request.data.get("appointment_id")
                )

            if is_paid is not None:
                application.is_paid = is_paid
            if is_notified is not None:
                application.is_notified = is_notified
            if link_sent is not None:
                application.link_sent = link_sent
            if is_deleted is not None:
                application.is_deleted = is_deleted

            application.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
