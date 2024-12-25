from django.contrib import admin

from .models import (
    Application,
    Appointment,
    DoctorDescription,
    HelpInfo,
    Specialization,
    User,
    UserStep,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "last_name",
        "first_name",
        "middle_name",
        "telegram_id",
        "telegram_username",
        "phone_number",
        "is_doctor",
    ]

    search_fields = ["last_name__iregex", "first_name__iregex", "middle_name__iregex"]

    list_filter = ["is_doctor"]


@admin.register(DoctorDescription)
class DoctorDescriptionAdmin(admin.ModelAdmin):
    list_display = [
        "doctor",
        "specialization",
        "consultation_price",
        "medical_degree",
        "work_experience",
        "about",
        "photo",
    ]

    search_fields = [
        "doctor__last_name__iregex",
        "doctor__first_name__iregex",
        "doctor__middle_name__iregex",
        "specialization__name__iregex",
    ]

    list_filter = ["specialization__name"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = User.objects.filter(is_doctor=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ["name"]

    search_fields = ["name__iregex"]

    list_filter = ["name"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "doctor_specialization",
        "patient",
        "appointment_time",
        "is_notified",
        "is_deleted",
    ]

    search_fields = [
        "doctor_specialization__doctor__last_name__iregex",
        "doctor_specialization__doctor__first_name__iregex",
        "doctor_specialization__doctor__middle_name__iregex",
    ]

    list_filter = ["doctor_specialization"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor_specialization__doctor__last_name=request.user.username)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor_specialization" and not request.user.is_superuser:
            kwargs["queryset"] = DoctorDescription.objects.filter(
                doctor__last_name=request.user.username
            )
        if db_field.name == "patient":
            if not request.user.is_superuser:
                kwargs["queryset"] = User.objects.filter(
                    last_name=request.user.username
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "appointment",
        "is_paid",
        "created_at",
        "link_sent",
        "is_notified",
        "is_deleted",
    ]
    list_filter = ["is_paid"]


@admin.register(UserStep)
class UserStepAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "telegram_username",
        "telegram_id",
        "select_specialization_step",
        "select_doctor_step",
        "select_date_step",
        "select_time_step",
        "user_info_step",
        "created_at",
        "is_notified",
    ]
