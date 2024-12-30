from django.contrib import admin
from .models import Patient, Doctor, Appointment

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_email', 'address', 'created_at', 'updated_at') 
    search_fields = ('first_name', 'last_name', 'user__email') 
    
    def get_email(self, obj):
        return obj.user.email 
    get_email.short_description = 'Email'

admin.site.register(Patient, PatientAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'image')

admin.site.register(Doctor, DoctorAdmin)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'status', 'patient', 'doctor', 'created_at')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')

