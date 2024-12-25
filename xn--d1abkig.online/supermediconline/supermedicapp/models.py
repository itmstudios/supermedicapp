from django.db import models


class User(models.Model):
    last_name = models.CharField(max_length=40, verbose_name="Фамилия")
    first_name = models.CharField(max_length=40, verbose_name="Имя")
    middle_name = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="Отчество"
    )
    telegram_id = models.BigIntegerField(null=True, unique=True)
    telegram_username = models.CharField(
        max_length=50, null=True, blank=True, unique=True
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Телефон"
    )
    is_doctor = models.BooleanField(default=False, verbose_name="Доктор")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name if self.middle_name else ' '}"


class Specialization(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"

    def __str__(self):
        return self.name


class DoctorDescription(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_description",
        verbose_name="Доктор",
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Специализация",
    )
    consultation_price = models.IntegerField(
        null=True, blank=True, verbose_name="Стоимость приема"
    )
    about = models.TextField(null=True, blank=True, verbose_name="Описание")
    medical_degree = models.TextField(
        default=None, null=True, blank=True, verbose_name="Мед. степень"
    )
    work_experience = models.TextField(
        default=None, null=True, blank=True, verbose_name="Стаж работы"
    )
    photo = models.ImageField(
        upload_to="doctors_photo", verbose_name="Фото", null=True, blank=True
    )

    class Meta:
        verbose_name = "Описание доктора"
        verbose_name_plural = "Описания докторов"

    def __str__(self):
        return f"{self.doctor} {self.specialization.name}"


class Appointment(models.Model):
    doctor_specialization = models.ForeignKey(
        DoctorDescription,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Доктор и специализация",
    )
    patient = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
        verbose_name="Пациент",
    )
    appointment_time = models.DateTimeField(verbose_name="Дата и время")
    is_notified = models.BooleanField(default=False, verbose_name="Уведомление")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.doctor_specialization} {self.appointment_time}"


class HelpInfo(models.Model):
    title = models.TextField(
        null=True, blank=True, default=None, verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Инфо"
        verbose_name_plural = "Инфо"


class Application(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, verbose_name="Запись"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    created_at = models.DateTimeField(null=True, blank=True, verbose_name="Создано")
    link_sent = models.BooleanField(default=False, verbose_name="Ссылка")
    is_notified = models.BooleanField(default=False, verbose_name="Уведомление")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class UserStep(models.Model):
    name = models.CharField(
        max_length=40, null=True, blank=True, default=None, verbose_name="Имя"
    )
    telegram_username = models.CharField(
        max_length=40, null=True, blank=True, default=None, verbose_name="Юзернейм"
    )
    telegram_id = models.BigIntegerField(null=True, blank=True, default=None)
    select_specialization_step = models.BooleanField(
        default=False, verbose_name="Выбор специализации"
    )
    select_doctor_step = models.BooleanField(default=False, verbose_name="Выбор врача")
    select_date_step = models.BooleanField(default=False, verbose_name="Выбор даты")
    select_time_step = models.BooleanField(default=False, verbose_name="Выбор времени")
    user_info_step = models.BooleanField(default=False, verbose_name="Ввод инфо")
    created_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время"
    )
    is_notified = models.BooleanField(default=False, verbose_name="Уведомление")
