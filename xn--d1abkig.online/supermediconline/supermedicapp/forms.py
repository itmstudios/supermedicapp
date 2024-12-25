from django import forms

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "last_name",
            "first_name",
            "middle_name",
            "phone_number",
        ]
