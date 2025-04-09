from rest_framework import serializers
from .models import User, Specialization, DoctorDescription, Appointment, HelpInfo, Application, UserStep

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDescription
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class HelpInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class UserStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStep
        fields = '__all__'
