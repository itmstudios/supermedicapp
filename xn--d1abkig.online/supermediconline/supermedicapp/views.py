import logging
import os
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import RedirectView, TemplateView, View
from dotenv import load_dotenv

from .models import (
    Application,
    Appointment,
    DoctorDescription,
    HelpInfo,
    Specialization,
    User,
    UserStep,
)

logger = logging.getLogger(__name__)

load_dotenv()


class HomeView(TemplateView):
    template_name = "supermedicapp/main_menu/start.html"


class DoctorsHomeView(TemplateView):
    template_name = "supermedicapp/main_menu/start_doc.html"


class SaveTgID(View):
    def post(self, request):
        name = request.POST.get("name")
        telegram_username = request.POST.get("telegram_username")
        telegram_id = request.POST.get("telegram_id")

        request.session["name"] = name
        request.session["telegram_username"] = telegram_username
        request.session["telegram_id"] = telegram_id

        return JsonResponse({"status": "success"})


class OurDoctorsView(View):
    template_name = "supermedicapp/main_menu/our_doctors.html"

    def post(self, request):
        return render(request, self.template_name)

    def get(self, request, specialization_id=None):
        context = {}
        if specialization_id is not None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor_descriptions = DoctorDescription.objects.filter(
                specialization_id=specialization_id,
            ).order_by("doctor__last_name", "doctor__first_name", "doctor__middle_name")
            for doctor_description in doctor_descriptions:
                doctor_description.doctor.first_name = (
                    doctor_description.doctor.first_name[:1] + "."
                )
                if doctor_description.doctor.middle_name:
                    doctor_description.doctor.middle_name = (
                        doctor_description.doctor.middle_name[:1] + "."
                    )
            context = {
                "specialization": specialization,
                "doctor_descriptions": doctor_descriptions,
            }
        return render(request, self.template_name, context=context)


class OurDoctorsSpecView(View):
    template_name = "supermedicapp/main_menu/our_doctors_specialization.html"

    def post(self, request):
        specializations = Specialization.objects.all().distinct().order_by("name")
        return render(request, self.template_name, {"specializations": specializations})


class OurDoctorsDescView(View):
    template_name = "supermedicapp/main_menu/our_doctors_description.html"

    def post(self, request, doctor_description_id: int):
        doctor_description = DoctorDescription.objects.filter(
            pk=doctor_description_id
        ).first()
        return render(
            request, self.template_name, {"doctor_description": doctor_description}
        )


class HelpInfoView(View):
    template_name = "supermedicapp/main_menu/help_info.html"

    def post(self, request):
        info = HelpInfo.objects.all()
        return render(request, self.template_name, {"info": info})


class TextToAdminView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return os.getenv("ADMIN_LINK")


def convert_date(date_str: str) -> datetime:
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    new_date = date_obj.strftime("%Y-%m-%d")
    return datetime.strptime(new_date, "%Y-%m-%d")


def convert_date_to_str(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    new_date = date_obj.strftime("%d.%m.%Y")
    return new_date


class MyAppointmentsView(View):
    template_name = "supermedicapp/patients_menu/my_appointments.html"

    def post(self, request):
        appointments = None
        telegram_id = request.session.get("telegram_id")
        user = User.objects.filter(telegram_id=telegram_id).first()

        if user:
            appointments = Appointment.objects.filter(
                patient=user,
                is_deleted=False,
            ).order_by("appointment_time")

        return render(request, self.template_name, {"appointments": appointments})


def create_new_track(request):
    name = request.session.get("name")
    telegram_username = request.session.get("telegram_username")
    telegram_id = request.session.get("telegram_id")
    try:
        track = UserStep.objects.create(
            name=name,
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            created_at=datetime.now(),
        )
    except Exception as e:
        logger.error(f'{e}')
        track = UserStep.objects.create(
            name='none',
            telegram_id=111,
            telegram_username='none',
            created_at=datetime.now(),
        )
    request.session["track_id"] = track.pk
    return track


class SelectSpecialistView(View):
    template_name = "supermedicapp/patients_menu/select_specialist.html"

    def post(self, request):
        create_new_track(request)
        return render(request, self.template_name)

    def get(
        self,
        request,
        specialization_id=None,
        doctor_id=None,
        appointment_date=None,
        appointment_time=None,
        appointment_id=None,
    ):
        if specialization_id is None:
            return render(request, self.template_name, context={})

        if doctor_id is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()

            track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
            track.select_specialization_step = True
            track.created_at = datetime.now()
            track.save()

            return render(
                request, self.template_name, context={"specialization": specialization}
            )

        if appointment_date is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor = User.objects.filter(pk=doctor_id).first()

            track = UserStep.objects.filter(pk=request.session.get("track_id")).first()
            track.select_doctor_step = True
            track.created_at = datetime.now()
            track.save()

            return render(
                request,
                self.template_name,
                context={"specialization": specialization, "doctor": doctor},
            )
        if appointment_time is None:
            specialization = Specialization.objects.filter(pk=specialization_id).first()
            doctor = User.objects.filter(pk=doctor_id).first()
            try:
                appointment_date = convert_date_to_str(date_str=appointment_date)
            except Exception as e:
                logger.error(e)
            finally:
                track_id = request.session.get("track_id")
                track = UserStep.objects.filter(pk=track_id).first()
                track.select_date_step = True
                track.created_at = datetime.now()
                track.save()
                return render(
                    request,
                    self.template_name,
                    context={
                        "specialization": specialization,
                        "doctor": doctor,
                        "appointment_date": appointment_date,
                    },
                )
        else:
            track_id = request.session.get("track_id")
            track = UserStep.objects.filter(pk=track_id).first()
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
            return render(
                request,
                self.template_name,
                context={
                    "specialization": specialization,
                    "doctor": doctor,
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time,
                },
            )


class SelectSpecializationView(View):
    template_name = "supermedicapp/patients_menu/select_specialization.html"

    def post(self, request):
        specializations = Specialization.objects.all().distinct().order_by("name")

        return render(request, self.template_name, {"specializations": specializations})


class SelectDoctorView(View):
    template_name = "supermedicapp/patients_menu/doctors_list.html"

    def post(self, request, specialization_id):
        doctor_descriptions = (
            DoctorDescription.objects.filter(
                doctor__is_doctor=True,
                specialization_id=specialization_id,
            )
            .distinct()
            .order_by("doctor__last_name", "doctor__first_name", "doctor__middle_name")
        )

        return render(
            request,
            self.template_name,
            {
                "doctor_descriptions": doctor_descriptions,
                "specialization_id": specialization_id,
            },
        )

    def get(self, request, specialization_id):
        doctor_descriptions = (
            DoctorDescription.objects.filter(
                doctor__is_doctor=True,
                specialization_id=specialization_id,
            )
            .distinct()
            .order_by("doctor__last_name", "doctor__first_name", "doctor__middle_name")
        )

        return render(
            request,
            self.template_name,
            {
                "doctor_descriptions": doctor_descriptions,
                "specialization_id": specialization_id,
            },
        )


class DoctorInfoView(View):
    template_name = "supermedicapp/patients_menu/doctors_info.html"

    def post(self, request, specialization_id, doctor_id):
        doctor_description = DoctorDescription.objects.filter(
            doctor_id=doctor_id,
            specialization_id=specialization_id,
        ).first()

        return render(
            request, self.template_name, {"doctor_description": doctor_description}
        )


class SelectDateView(View):
    template_name = "supermedicapp/patients_menu/select_date.html"

    def post(self, request, specialization_id, doctor_id):
        return render(
            request,
            self.template_name,
            context={"specialization_id": specialization_id, "doctor_id": doctor_id},
        )


def get_appointment_dates(request):
    specialization_id = request.POST.get("specialization_id")
    doctor_id = request.POST.get("doctor_id")

    appointment_dates = Appointment.objects.filter(
        doctor_specialization__specialization_id=specialization_id,
        doctor_specialization__doctor_id=doctor_id,
        patient__isnull=True,
        appointment_time__gt=datetime.now(),
        is_deleted=False,
    ).values_list("appointment_time", flat=True)

    date_strings = [
        appointment_date.strftime("%Y-%m-%d") for appointment_date in appointment_dates
    ]

    return JsonResponse(date_strings, safe=False)


class SelectTimeView(View):
    template_name = "supermedicapp/patients_menu/select_time.html"

    def post(self, request, specialization_id, doctor_id, appointment_date):
        appointments = []

        try:
            # date = datetime.strptime(appointment_date, "%Y-%m-%d")
            date = convert_date(date_str=appointment_date)
        except Exception as e:
            logger.error(f"An error in SelectTimeView: {e}")
        else:
            appointments = Appointment.objects.filter(
                doctor_specialization__doctor_id=doctor_id,
                doctor_specialization__specialization_id=specialization_id,
                patient__isnull=True,
                appointment_time__date=date,
                is_deleted=False,
            ).order_by("appointment_time")

        return render(
            request,
            self.template_name,
            {
                "appointments": appointments,
                "appointment_date": appointment_date,
                "specialization_id": specialization_id,
                "doctor_id": doctor_id,
            },
        )


class GetUserInfoView(View):
    template_name = "supermedicapp/patients_menu/confirm_appointment.html"

    def post(self, request):
        telegram_id = request.session.get("telegram_id")
        appointment_id = request.session.get("appointment_id")
        specialization_id = request.session.get("specialization_id")
        doctor_id = request.session.get("doctor_id")
        appointment_date = request.session.get("appointment_date")
        appointment_time = request.session.get("appointment_time")
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except Exception as e:
            logger.error(f"An error in GetUserInfoView get user: {e}")
            user = None
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Exception as e:
            logger.error(f"An error in GetUserInfoView get appointment: {e}")
            appointment = None

        return render(
            request,
            self.template_name,
            {
                "appointment": appointment,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "specialization_id": specialization_id,
                "doctor_id": doctor_id,
                "user": user,
            },
        )

    def get(self, request):
        telegram_id = request.session.get("telegram_id")
        appointment_id = request.session.get("appointment_id")
        specialization_id = request.session.get("specialization_id")
        doctor_id = request.session.get("doctor_id")
        appointment_date = request.session.get("appointment_date")
        appointment_time = request.session.get("appointment_time")
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except Exception as e:
            logger.error(f"An error in GetUserInfoView get user: {e}")
            user = None
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Exception as e:
            logger.error(f"An error in GetUserInfoView get appointment: {e}")
            appointment = None

        return render(
            request,
            self.template_name,
            {
                "appointment": appointment,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "specialization_id": specialization_id,
                "doctor_id": doctor_id,
                "user": user,
            },
        )


def get_or_create_user(
    last_name: str,
    first_name: str,
    phone_number: str,
    telegram_id: int,
    telegram_username=None,
    middle_name=None,
):
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": middle_name,
            "phone_number": phone_number,
            "telegram_username": telegram_username,
        },
    )
    return user


class SubmitAppointmentView(View):
    template_name = "supermedicapp/patients_menu/submit_dropdown.html"

    def post(self, request):
        track_id = request.session.get("track_id")
        track = UserStep.objects.filter(pk=track_id).first()
        if track:
            track.user_info_step = True
            track.created_at = datetime.now()
            track.save()

        user = get_or_create_user(
            last_name=request.POST.get("user_last_name"),
            first_name=request.POST.get("user_first_name"),
            middle_name=request.POST.get("user_middle_name"),
            phone_number=request.POST.get("user_phone_number"),
            telegram_id=request.POST.get("user_telegram_id"),
            telegram_username=request.POST.get("user_telegram_username"),
        )

        try:
            appointment = Appointment.objects.filter(
                pk=request.session.get("appointment_id"),
                patient__isnull=True,
            ).first()

        except Exception as e:
            logger.error(f"An error in SubmitAppointmentView: {e}")
            return JsonResponse({"result": False})

        else:
            appointment.patient = user
            appointment.save()

            Application.objects.create(
                appointment=appointment, created_at=datetime.now()
            )

            return JsonResponse({"result": True})


def appointment_payment(request):
    pass


def payment_alerts(request):
    return HttpResponse(200)


class MyPatientsView(View):
    template_name = "supermedicapp/doctors_menu/my_patients.html"

    def post(self, request, telegram_id):
        appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=False,
            is_deleted=False,
        ).order_by("appointment_time")
        return render(request, self.template_name, {"appointments": appointments})


class UpdateWorkTimeView(View):
    template_name = "supermedicapp/doctors_menu/calendar.html"

    def post(self, request, telegram_id):
        return render(request, self.template_name, {"telegram_id": telegram_id})

    def get(self, request, telegram_id):
        return render(request, self.template_name, {"telegram_id": telegram_id})


class TimePreView(View):
    template_name = "supermedicapp/doctors_menu/time_preview.html"

    def get(self, request, telegram_id, appointment_date):
        free_appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=True,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time__time")
        booked_appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=False,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time__time")

        return render(
            request,
            self.template_name,
            {
                "telegram_id": telegram_id,
                "appointment_date": appointment_date,
                "free_appointments": free_appointments,
                "booked_appointments": booked_appointments,
            },
        )


class AddWorkHoursView(View):
    template_name = "supermedicapp/doctors_menu/add_work_hours.html"

    def post(self, request, telegram_id, appointment_date):
        return render(
            request,
            self.template_name,
            {"telegram_id": telegram_id, "appointment_date": appointment_date},
        )


class SuccessAddView(View):
    def post(self, request, telegram_id, appointment_date):
        hours = request.POST.getlist("hours")
        minutes = request.POST.getlist("minutes")

        for hour, minute in zip(hours, minutes):
            appointment_time = hour + ":" + minute

            appointment_time = datetime.combine(
                datetime.strptime(appointment_date, "%Y-%m-%d").date(),
                datetime.strptime(appointment_time, "%H:%M").time(),
            )

            try:
                doctor_description = DoctorDescription.objects.filter(
                    doctor__telegram_id=telegram_id
                ).first()
                Appointment.objects.get_or_create(
                    doctor_specialization=doctor_description,
                    appointment_time=appointment_time,
                )

            except:
                return JsonResponse({"result": False})

        return JsonResponse({"result": True})


class DeleteWorkHoursView(View):
    template_name = "supermedicapp/doctors_menu/delete_work_hours.html"

    def post(self, request, telegram_id, appointment_date):
        appointments = Appointment.objects.filter(
            doctor_specialization__doctor__telegram_id=telegram_id,
            patient__isnull=True,
            appointment_time__date=appointment_date,
            is_deleted=False,
        ).order_by("appointment_time__time")

        return render(
            request,
            self.template_name,
            {
                "appointments": appointments,
                "telegram_id": telegram_id,
                "appointment_date": appointment_date,
            },
        )


class SuccessDeleteView(View):
    def post(self, request):
        appointments_data = request.POST.get("appointments")
        appointments = [int(num) for num in appointments_data.split(",")]
        response = True
        try:
            Appointment.objects.filter(id__in=appointments).update(is_deleted=True)
        except Exception as e:
            logger.error(e)
            response = False

        return JsonResponse({"result": response})


def get_appointment_dates_doc(request):
    telegram_id = request.POST.get("telegram_id")

    appointment_dates = Appointment.objects.filter(
        doctor_specialization__doctor__telegram_id=telegram_id,
        appointment_time__gt=datetime.now(),
        is_deleted=False,
    ).values_list("appointment_time", flat=True)

    date_strings = [
        appointment_date.strftime("%Y-%m-%d") for appointment_date in appointment_dates
    ]

    return JsonResponse(date_strings, safe=False)
