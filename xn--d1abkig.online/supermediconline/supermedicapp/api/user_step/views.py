from datetime import datetime, timedelta

import pytz
import supermedicapp.api.user_step.serializers as serializers
import supermedicapp.models as models
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserStepView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='select_specialization_step',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'select_specialization_step_example_default',
                        summary='Select specialization',
                        value='',
                    ),
                    OpenApiExample(
                        'select_specialization_step_example_false',
                        summary='Do not select specialization',
                        value='False',
                    ),
                ]
            ),
            OpenApiParameter(
                name='select_doctor_step',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'select_doctor_step_example_default',
                        summary='Select doctor',
                        value='',
                    ),
                    OpenApiExample(
                        'select_doctor_step_example_false',
                        summary='Do not select doctor',
                        value='False',
                    ),
                ]
            ),
            OpenApiParameter(
                name='select_date_step',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'select_date_step_example_default',
                        summary='Select date',
                        value='',
                    ),
                    OpenApiExample(
                        'select_date_step_example_false',
                        summary='Do not select date',
                        value='False',
                    ),
                ]
            ),
            OpenApiParameter(
                name='select_time_step',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'select_time_step_example_default',
                        summary='Select time',
                        value='',
                    ),
                    OpenApiExample(
                        'select_time_step_example_false',
                        summary='Do not select time',
                        value='False',
                    ),
                ]
            ),
            OpenApiParameter(
                name='user_info_step',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'select_info_step_example_default',
                        summary='Select info',
                        value='',
                    ),
                    OpenApiExample(
                        'select_info_step_example_false',
                        summary='Do not select info',
                        value='False',
                    ),
                ]
            ),
        ],
        responses={
            200: serializers.UserStepGetSerializer,
            400: OpenApiResponse(
                description="Error message",
                response=serializers.UserStepErrorResponseSerializer,
            )
        },
    )
    def get(self, request):
        select_specialization_step = request.GET.get("select_specialization_step")
        select_doctor_step = request.GET.get("select_doctor_step")
        select_date_step = request.GET.get("select_date_step")
        select_time_step = request.GET.get("select_time_step")
        user_info_step = request.GET.get("user_info_step")
        current_time = datetime.now(pytz.timezone("Europe/Moscow"))
        # current_time = datetime.now()
        canceled_time = current_time - timedelta(minutes=5)
        try:
            if select_specialization_step == 'False':
                user_step = models.UserStep.objects.filter(
                    select_specialization_step=False,
                    is_notified=False,
                    created_at__lt=canceled_time,
                )
                serializer = serializers.UserStepGetSerializer(user_step, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if select_doctor_step == 'False':
                user_step = models.UserStep.objects.filter(
                    select_specialization_step=select_specialization_step,
                    select_doctor_step=False,
                    is_notified=False,
                    created_at__lt=canceled_time,
                )
                serializer = serializers.UserStepGetSerializer(user_step, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if select_date_step == 'False':
                user_step = models.UserStep.objects.filter(
                    select_doctor_step=select_doctor_step,
                    select_date_step=False,
                    is_notified=False,
                    created_at__lt=canceled_time,
                )
                serializer = serializers.UserStepGetSerializer(user_step, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if select_time_step == 'False':
                user_step = models.UserStep.objects.filter(
                    select_date_step=select_date_step,
                    select_time_step=False,
                    is_notified=False,
                    created_at__lt=canceled_time,
                )
                serializer = serializers.UserStepGetSerializer(user_step, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if user_info_step == 'False':
                user_step = models.UserStep.objects.filter(
                    select_time_step=select_time_step,
                    user_info_step=False,
                    is_notified=False,
                    created_at__lt=canceled_time,
                )
                serializer = serializers.UserStepGetSerializer(user_step, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=serializers.UserStepUpdateSerializer,
        responses={
            200: OpenApiResponse(description="Ok"),
            400: OpenApiResponse(
                description="Error message",
                response=serializers.UserStepErrorResponseSerializer,
            ),
        },
    )
    def patch(self, request):
        serializer = serializers.UserStepUpdateSerializer(data=request.data)
        if serializer.is_valid():
            step_id = serializer.validated_data.get("id")
            is_notified = serializer.validated_data.get("is_notified")
            try:
                user_step = models.UserStep.objects.get(pk=step_id)
                user_step.is_notified = is_notified
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_step.save()
                return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
