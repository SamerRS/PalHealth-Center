from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Doctor, Appointment, Patient
from .forms import AppointmentForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError 


def home(request):
    doctors = Doctor.objects.all()  
    return render(request, 'core/index.html', {'doctors': doctors})

def about(request):
    return render(request, 'core/about.html')

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'core/doctor_list.html', {'doctors': doctors})

@login_required(login_url='login_register')
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Get the Patient instance associated with the current user
                patient = Patient.objects.get(user=request.user)

                # Save the appointment with the Patient instance
                appointment = form.save(commit=False)
                appointment.patient = patient
                appointment.save()

                messages.success(request, "Your appointment has been successfully booked!")
                return redirect('home')  # Redirect to home page or any other page
            except Patient.DoesNotExist:
                messages.error(request, "Please complete your profile to book an appointment.")
                return redirect('home')
    else:
        form = AppointmentForm()

    return render(request, 'core/appointment_create.html', {'form': form})


def login_register(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials.")

        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()

                if not Patient.objects.filter(user=user).exists():
                    Patient.objects.create(
                        user=user,
                        first_name=register_form.cleaned_data.get('first_name'),
                        last_name=register_form.cleaned_data.get('last_name'),
                        email=register_form.cleaned_data.get('email'),
                        address=register_form.cleaned_data.get('address'),
                    )

                login(request, user)
                messages.success(request, f"Welcome, {user.first_name} {user.last_name}!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors in the registration form.")

    return render(request, 'core/login_register.html', {
        'login_form': login_form,
        'register_form': register_form,
    })




def LogoutView(request):
    logout(request)
    return redirect('home')
