from django import forms
from .models import Appointment, Patient
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Save the user instance
        user = super().save(commit=False)
        if commit:
            user.save()

        # Create a Patient instance linked to the User
        Patient.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            address=self.cleaned_data['address']
        )
        return user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'doctor'] 

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date < timezone.now():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return appointment_date


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-pill shadow-sm',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-pill shadow-sm',
            'placeholder': 'Enter your password'
        })
    )
