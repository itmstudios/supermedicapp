from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import supermedicapp.models as models
import supermedicapp.api.user.serializers as serializers


class UserView(APIView):
    def get(self, request):
        user_id = request.GET.get("user_id")
        try:
            user = models.User.objects.filter(pk=user_id).first()
            serializer = serializers.UserGetSerializer(user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
