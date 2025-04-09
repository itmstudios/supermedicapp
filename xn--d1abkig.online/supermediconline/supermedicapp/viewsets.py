import logging
import os
from datetime import datetime

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Application,
    Appointment,
    DoctorDescription,
    HelpInfo,
    Specialization,
    User,
    UserStep,
)
from .serializers import (
    ApplicationSerializer,
    AppointmentSerializer,
    DoctorDescriptionSerializer,
    HelpInfoSerializer,
    SpecializationSerializer,
    UserSerializer,
    UserStepSerializer,
)

logger = logging.getLogger(__name__)


class EmptySerializer(serializers.Serializer):
    pass


def convert_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%d.%m.%Y")


def convert_date_to_str(date_str: str) -> str:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except Exception as e:
        logger.error(e)
        return date_str


def create_new_track(request):
    name = request.session.get("name")
    telegram_username = request.session.get("telegram_username")
    telegram_id = request.session.get("telegram_id")
    try:
        track = UserStep.objects.create(
            name=name,
            telegram_username=telegram_username,
            telegram_id=telegram_id,
            created_at=datetime.now(),
        )
    except Exception as e:
        logger.error(e)
        track = UserStep.objects.create(
            name="none",
            telegram_username="none",
            telegram_id=111,
            created_at=datetime.now(),
        )
    request.session["track_id"] = track.pk
    return track


def get_or_create_user(data):
    user, created = User.objects.get_or_create(
        telegram_id=data.get("user_telegram_id"),
        defaults={
            "last_name": data.get("user_last_name"),
            "first_name": data.get("user_first_name"),
            "middle_name": data.get("user_middle_name"),
            "phone_number": data.get("user_phone_number"),
            "telegram_username": data.get("user_telegram_username"),
        },
    )
    return user


class HomeViewSet(viewsets.ViewSet):
    serializer_class = EmptySerializer

    @action(detail=False, methods=["get"])
    def home(self, request):
        return Response({"message": "welcome"})

    @action(detail=False, methods=["get"])
    def doctors_home(self, request):
        return Response({"message": "doctors home"})

    @action(detail=False, methods=["get"])
    def text_to_admin(self, request):
        link = os.getenv("ADMIN_LINK", "")
        return Response({"admin_link": link})


class UserViewSet(viewsets.ViewSet):
    serializer_class = EmptySerializer

    @action(detail=False, methods=["post"])
    def save_tg_id(self, request):
        request.session["name"] = request.data.get("name")
        request.session["telegram_username"] = request.data.get("telegram_username")
        request.session["telegram_id"] = request.data.get("telegram_id")
        return Response({"status": "success"})

    @action(detail=False, methods=["get", "post"])
    def get_user_info(self, request):
        telegram_id = request.session.get("telegram_id")
        appointment_id = request.session.get("appointment_id")
        specialization_id = request.session.get("specialization_id")
        doctor_id = request.session.get("doctor_id")
        appointment_date = request.session.get("appointment_date")
        appointment_time = request.session.get("appointment_time")
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except Exception as e:
            logger.error(e)
            user = None
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Exception as e:
            logger.error(e)
            appointment = None
        user_data = UserSerializer(user).data if user else None
        appointment_data = (
            AppointmentSerializer(appointment).data if appointment else None
        )
        return Response(
            {
                "appointment": appointment_data,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "specialization_id": specialization_id,
                "doctor_id": doctor_id,
                "user": user_data,
            }
        )


class SpecializationViewSet(viewsets.ViewSet):
    serializer_class = EmptySerializer

    @action(detail=False, methods=["post"])
    def our_doctors_spec(self, request):
        specializations = Specialization.objects.all().distinct().order_by("name")
        serializer = SpecializationSerializer(specializations, many=True)
        return Response({"specializations": serializer.data})

    @action(detail=False, methods=["post"])
    def select_specialization(self, request):
        specializations = Specialization.objects.all().distinct().order_by("name")
        serializer = SpecializationSerializer(specializations, many=True)
        return Response({"specializations": serializer.data})


class DoctorViewSet(viewsets.ViewSet):
    serializer_class = EmptySerializer

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="our_doctors(?:/(?P<specialization_id>\\d+))?",
    )
    def our_doctors(self, request, specialization_id=None):
        if specialization_id is not None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor_descriptions = DoctorDescription.objects.filter(
                specialization_id=specialization_id
            ).order_by("doctor__last_name", "doctor__first_name", "doctor__middle_name")
            for dd in doctor_descriptions:
                dd.doctor.first_name = dd.doctor.first_name[:1] + "."
                if dd.doctor.middle_name:
                    dd.doctor.middle_name = dd.doctor.middle_name[:1] + "."
            spec_data = (
                SpecializationSerializer(specialization).data
                if specialization
                else None
            )
            dd_serializer = DoctorDescriptionSerializer(doctor_descriptions, many=True)
            return Response(
                {"specialization": spec_data, "doctor_descriptions": dd_serializer.data}
            )
        return Response({})

    @action(
        detail=False,
        methods=["post"],
        url_path="our_doctors_desc/(?P<doctor_description_id>\\d+)",
    )
    def our_doctors_desc(self, request, doctor_description_id=None):
        doctor_description = DoctorDescription.objects.filter(
            pk=doctor_description_id
        ).first()
        serializer = DoctorDescriptionSerializer(doctor_description)
        return Response({"doctor_description": serializer.data})

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="select_doctor/(?P<specialization_id>\\d+)",
    )
    def select_doctor(self, request, specialization_id=None):
        doctor_descriptions = (
            DoctorDescription.objects.filter(
                doctor__is_doctor=True, specialization_id=specialization_id
            )
            .distinct()
            .order_by("doctor__last_name", "doctor__first_name", "doctor__middle_name")
        )
        serializer = DoctorDescriptionSerializer(doctor_descriptions, many=True)
        return Response(
            {
                "doctor_descriptions": serializer.data,
                "specialization_id": specialization_id,
            }
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="doctor_info/(?P<specialization_id>\\d+)/(?P<doctor_id>\\d+)",
    )
    def doctor_info(self, request, specialization_id=None, doctor_id=None):
        doctor_description = DoctorDescription.objects.filter(
            doctor_id=doctor_id, specialization_id=specialization_id
        ).first()
        serializer = DoctorDescriptionSerializer(doctor_description)
        return Response({"doctor_description": serializer.data})

    @action(
        detail=False, methods=["post"], url_path="my_patients/(?P<telegram_id>\\d+)"
    )
    def my_patients(self, request, telegram_id=None):
        appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=False,
            is_deleted=False,
        ).order_by("appointment_time")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"appointments": serializer.data})

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="update_work_time/(?P<telegram_id>\\d+)",
    )
    def update_work_time(self, request, telegram_id=None):
        return Response({"telegram_id": telegram_id})

    @action(
        detail=False,
        methods=["get"],
        url_path="time_preview/(?P<telegram_id>\\d+)/(?P<appointment_date>[^/]+)",
    )
    def time_preview(self, request, telegram_id=None, appointment_date=None):
        free_appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=True,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time")
        booked_appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=False,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time")
        free_ser = AppointmentSerializer(free_appointments, many=True)
        booked_ser = AppointmentSerializer(booked_appointments, many=True)
        return Response(
            {
                "telegram_id": telegram_id,
                "appointment_date": appointment_date,
                "free_appointments": free_ser.data,
                "booked_appointments": booked_ser.data,
            }
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="add_work_hours/(?P<telegram_id>\\d+)/(?P<appointment_date>[^/]+)",
    )
    def add_work_hours(self, request, telegram_id=None, appointment_date=None):
        return Response(
            {"telegram_id": telegram_id, "appointment_date": appointment_date}
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="success_add/(?P<telegram_id>\\d+)/(?P<appointment_date>[^/]+)",
    )
    def success_add(self, request, telegram_id=None, appointment_date=None):
        hours = request.data.getlist("hours")
        minutes = request.data.getlist("minutes")
        result = True
        for hour, minute in zip(hours, minutes):
            appointment_time_str = hour + ":" + minute
            appointment_time = datetime.combine(
                datetime.strptime(appointment_date, "%Y-%m-%d").date(),
                datetime.strptime(appointment_time_str, "%H:%M").time(),
            )
            try:
                doctor_description = DoctorDescription.objects.filter(
                    doctor__telegram_id=telegram_id
                ).first()
                Appointment.objects.get_or_create(
                    doctor_specialization=doctor_description,
                    appointment_time=appointment_time,
                )
            except Exception:
                result = False
        return Response({"result": result})

    @action(
        detail=False,
        methods=["post"],
        url_path="delete_work_hours/(?P<telegram_id>\\d+)/(?P<appointment_date>[^/]+)",
    )
    def delete_work_hours(self, request, telegram_id=None, appointment_date=None):
        appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=True,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(
            {
                "appointments": serializer.data,
                "telegram_id": telegram_id,
                "appointment_date": appointment_date,
            }
        )

    @action(detail=False, methods=["post"])
    def success_delete(self, request):
        appointments_data = request.data.get("appointments", "")
        appointments_ids = [int(i) for i in appointments_data.split(",") if i]
        result = True
        try:
            Appointment.objects.filter(id__in=appointments_ids).update(is_deleted=True)
        except Exception as e:
            logger.error(e)
            result = False
        return Response({"result": result})


class AppointmentViewSet(viewsets.ViewSet):
    serializer_class = EmptySerializer

    @action(detail=False, methods=["post"])
    def my_appointments(self, request):
        telegram_id = request.session.get("telegram_id")
        user = User.objects.filter(telegram_id=telegram_id).first()
        appointments = (
            Appointment.objects.filter(patient=user, is_deleted=False).order_by(
                "appointment_time"
            )
            if user
            else []
        )
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"appointments": serializer.data})

    @action(
        detail=False,
        methods=["get", "post"],
        url_path="select_specialist(?:/(?P<specialization_id>\\d+))?(?:/(?P<doctor_id>\\d+))?(?:/(?P<appointment_date>[^/]+))?(?:/(?P<appointment_time>[^/]+))?(?:/(?P<appointment_id>\\d+))?",
    )
    def select_specialist(
        self,
        request,
        specialization_id=None,
        doctor_id=None,
        appointment_date=None,
        appointment_time=None,
        appointment_id=None,
    ):
        if specialization_id is None:
            return Response({})
        if doctor_id is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            create_new_track(request)
            spec_data = (
                SpecializationSerializer(specialization).data
                if specialization
                else None
            )
            return Response({"specialization": spec_data})
        if appointment_date is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor = User.objects.filter(pk=doctor_id).first()
            track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
            if track:
                track.select_doctor_step = True
                track.created_at = datetime.now()
                track.save()
            spec_data = (
                SpecializationSerializer(specialization).data
                if specialization
                else None
            )
            doctor_data = UserSerializer(doctor).data if doctor else None
            return Response({"specialization": spec_data, "doctor": doctor_data})
        if appointment_time is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor = User.objects.filter(pk=doctor_id).first()
            try:
                appointment_date_str = convert_date_to_str(appointment_date)
            except Exception as e:
                logger.error(e)
                appointment_date_str = appointment_date
            track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
            if track:
                track.select_date_step = True
                track.created_at = datetime.now()
                track.save()
            spec_data = (
                SpecializationSerializer(specialization).data
                if specialization
                else None
            )
            doctor_data = UserSerializer(doctor).data if doctor else None
            return Response(
                {
                    "specialization": spec_data,
                    "doctor": doctor_data,
                    "appointment_date": appointment_date_str,
                }
            )
        else:
            track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
            if track:
                track.select_time_step = True
                track.created_at = datetime.now()
                track.save()
            request.session["appointment_id"] = appointment_id
            request.session["specialization_id"] = specialization_id
            request.session["doctor_id"] = doctor_id
            request.session["appointment_date"] = appointment_date
            request.session["appointment_time"] = appointment_time
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor = User.objects.filter(pk=doctor_id).first()
            spec_data = (
                SpecializationSerializer(specialization).data
                if specialization
                else None
            )
            doctor_data = UserSerializer(doctor).data if doctor else None
            return Response(
                {
                    "specialization": spec_data,
                    "doctor": doctor_data,
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time,
                }
            )

    @action(
        detail=False,
        methods=["post"],
        url_path="select_date/(?P<specialization_id>\\d+)/(?P<doctor_id>\\d+)",
    )
    def select_date(self, request, specialization_id=None, doctor_id=None):
        return Response(
            {"specialization_id": specialization_id, "doctor_id": doctor_id}
        )

    @action(detail=False, methods=["post"])
    def get_appointment_dates(self, request):
        specialization_id = request.data.get("specialization_id")
        doctor_id = request.data.get("doctor_id")
        appointment_dates = Appointment.objects.filter(
            doctor_specialization__specialization_id=specialization_id,
            doctor_specialization__doctor_id=doctor_id,
            patient__isnull=True,
            appointment_time__gt=datetime.now(),
            is_deleted=False,
        ).values_list("appointment_time", flat=True)
        date_strings = [ad.strftime("%Y-%m-%d") for ad in appointment_dates]
        return Response(date_strings)

    @action(
        detail=False,
        methods=["post"],
        url_path="select_time/(?P<specialization_id>\\d+)/(?P<doctor_id>\\d+)/(?P<appointment_date>[^/]+)",
    )
    def select_time(
        self, request, specialization_id=None, doctor_id=None, appointment_date=None
    ):
        try:
            date_obj = convert_date(appointment_date)
        except Exception as e:
            logger.error(e)
            date_obj = appointment_date
        appointments = Appointment.objects.filter(
            doctor_specialization__doctor_id=doctor_id,
            doctor_specialization__specialization_id=specialization_id,
            patient__isnull=True,
            appointment_time__date=date_obj,
            is_deleted=False,
        ).order_by("appointment_time")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(
            {
                "appointments": serializer.data,
                "appointment_date": appointment_date,
                "specialization_id": specialization_id,
                "doctor_id": doctor_id,
            }
        )

    @action(detail=False, methods=["post"])
    def submit_appointment(self, request):
        track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
        if track:
            track.user_info_step = True
            track.created_at = datetime.now()
            track.save()
        user = get_or_create_user(request.data)
        appointment = Appointment.objects.filter(
            pk=request.session.get("appointment_id"), patient__isnull=True
        ).first()
        if not appointment:
            return Response({"result": False})
        appointment.patient = user
        appointment.save()
        Application.objects.create(appointment=appointment, created_at=datetime.now())
        return Response({"result": True})

    @action(detail=False, methods=["post"])
    def appointment_payment(self, request):
        return Response({"result": "not_implemented"})

    @action(detail=False, methods=["post"])
    def payment_alerts(self, request):
        return Response({"status": "ok"})

    @action(detail=False, methods=["post"])
    def get_appointment_dates_doc(self, request):
        telegram_id = request.data.get("telegram_id")
        appointment_dates = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            appointment_time__gt=datetime.now(),
            is_deleted=False,
        ).values_list("appointment_time", flat=True)
        date_strings = [ad.strftime("%Y-%m-%d") for ad in appointment_dates]
        return Response(date_strings)
