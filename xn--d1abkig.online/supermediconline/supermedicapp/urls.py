from django.urls import path

from . import views
from .api.application import views as application_views
from .api.appointment import views as appointment_views
from .api.doctor_description import views as doctor_views
from .api.user import views as user_views
from .api.user_step import views as user_step_views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("save_tg_id/", views.SaveTgID.as_view(), name="save_tg_id"),
    path(
        "our_doctors/<int:specialization_id>/",
        views.OurDoctorsView.as_view(),
        name="our_doctors",
    ),
    path("our_doctors/", views.OurDoctorsView.as_view(), name="our_doctors"),
    path(
        "our_doctors_specialization/",
        views.OurDoctorsSpecView.as_view(),
        name="our_doctors_specialization",
    ),
    path(
        "our_doctors_description/<int:doctor_description_id>/",
        views.OurDoctorsDescView.as_view(),
        name="our_doctors_description",
    ),
    path("help_info/", views.HelpInfoView.as_view(), name="help_info"),
    path("text_to_admin/", views.TextToAdminView.as_view(), name="text_to_admin"),
    path(
        "my_appointments/", views.MyAppointmentsView.as_view(), name="my_appointments"
    ),
    path(
        "select_specialist/<int:specialization_id>/<int:doctor_id>/<str:appointment_date>/<str:appointment_time>/<int:appointment_id>/",
        views.SelectSpecialistView.as_view(),
        name="select_specialist",
    ),
    path(
        "select_specialist/<int:specialization_id>/<int:doctor_id>/<str:appointment_date>/",
        views.SelectSpecialistView.as_view(),
        name="select_specialist",
    ),
    path(
        "select_specialist/<int:specialization_id>/<int:doctor_id>/",
        views.SelectSpecialistView.as_view(),
        name="select_specialist",
    ),
    path(
        "select_specialist/<int:specialization_id>/",
        views.SelectSpecialistView.as_view(),
        name="select_specialist",
    ),
    path(
        "select_specialist/",
        views.SelectSpecialistView.as_view(),
        name="select_specialist",
    ),
    path(
        "select_specialization/",
        views.SelectSpecializationView.as_view(),
        name="select_specialization",
    ),
    path(
        "select_doctor/<int:specialization_id>/",
        views.SelectDoctorView.as_view(),
        name="select_doctor",
    ),
    path(
        "doctors_info/<int:specialization_id>/<int:doctor_id>/",
        views.DoctorInfoView.as_view(),
        name="doctors_info",
    ),
    path(
        "select_date/<int:specialization_id>/<int:doctor_id>/",
        views.SelectDateView.as_view(),
        name="select_date",
    ),
    path(
        "get_appointment_dates/",
        views.get_appointment_dates,
        name="get_appointment_dates",
    ),
    path(
        "select_time/<int:specialization_id>/<int:doctor_id>/<str:appointment_date>/",
        views.SelectTimeView.as_view(),
        name="select_time",
    ),
    path("get_user_info/", views.GetUserInfoView.as_view(), name="get_user_info"),
    path(
        "submit_appointment/",
        views.SubmitAppointmentView.as_view(),
        name="submit_appointment",
    ),
    path("appointment_payment/", views.appointment_payment, name="payment_alerts"),
    path("payment_alerts/", views.payment_alerts, name="payment_alerts"),
    path("doctors/", views.DoctorsHomeView.as_view(), name="doctors"),
    path(
        "my_patients/<int:telegram_id>/",
        views.MyPatientsView.as_view(),
        name="my_patients",
    ),
    path(
        "update_work_time/<int:telegram_id>/",
        views.UpdateWorkTimeView.as_view(),
        name="update_work_time",
    ),
    path(
        "time_preview/<int:telegram_id>/<str:appointment_date>/",
        views.TimePreView.as_view(),
        name="time_preview",
    ),
    path(
        "time_preview/<int:telegram_id>/<str:appointment_date>/",
        views.TimePreView.as_view(),
        name="time_preview",
    ),
    path(
        "delete_work_hours/<int:telegram_id>/<str:appointment_date>/",
        views.DeleteWorkHoursView.as_view(),
        name="delete_work_hours",
    ),
    path("success_delete/", views.SuccessDeleteView.as_view(), name="success_delete"),
    path(
        "add_work_hours/<int:telegram_id>/<str:appointment_date>/",
        views.AddWorkHoursView.as_view(),
        name="add_work_hours",
    ),
    path(
        "success_change_time/<int:telegram_id>/<str:appointment_date>/",
        views.SuccessAddView.as_view(),
        name="success_change_time",
    ),
    path(
        "get_appointment_dates_doc/",
        views.get_appointment_dates_doc,
        name="get_appointment_dates_doc",
    ),
]


urlpatterns_api = [
    path("api/application/", application_views.ApplicationView.as_view()),
    path("api/appointment/", appointment_views.AppointmentView.as_view()),
    path("api/doctor_description/", doctor_views.DoctorDescriptionView.as_view()),
    path("api/user/", user_views.UserView.as_view()),
    path("api/user_step/", user_step_views.UserStepView.as_view()),
]

urlpatterns += urlpatterns_api

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'home', viewsets.HomeViewSet, basename='home')
router.register(r'user', viewsets.UserViewSet, basename='user')
router.register(r'specialization', viewsets.SpecializationViewSet, basename='specialization')
router.register(r'doctor', viewsets.DoctorViewSet, basename='doctor')
router.register(r'appointment', viewsets.AppointmentViewSet, basename='appointment')

urlpatterns += [
    path('api/', include(router.urls)),
]
