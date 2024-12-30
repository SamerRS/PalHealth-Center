from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'), 
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('doctors/', views.doctor_list, name='doctor_list'),  
    path('about/', views.about , name='about'),
    path('login-register/', views.login_register, name='login_register'), 
    path('logout/', views.LogoutView, name='logout'),

]


























if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)