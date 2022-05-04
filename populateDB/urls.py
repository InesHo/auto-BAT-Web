from django.urls import path
from .views import show_experiment, show_experimentfile, edit, home, register, experiment, experimenter, institute, department, cytometer, device, marker, donor, panel, filetype, experimentfile
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetDoneView)

app_name = 'populateDB'

urlpatterns = [
    
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('home/', home, name='home'),
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='auth/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='auth/password_change_form.html'), name='password_change'),
    path('password_change/dond/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='auth/password_reset_form.html',
        email_template_name='auth/password_reset_email.html',
        success_url=reverse_lazy('populateDB:password_reset_done')), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        success_url=reverse_lazy('auth:login')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    
    path('add_experiment/', experiment, name='add_experiment'),
    path('add_experimenter/', experimenter, name='add_experimenter'),
    path('add_institute/', institute, name='add_institute'),
    path('add_department/', department, name='add_department'),
    path('add_cytometer/', cytometer, name='add_cytometer'),
    path('add_device/', device, name='add_device'),
    path('add_marker/', marker, name='add_marker'),
    path('add_donor/', donor, name='add_donor'),
    path('add_panel/', panel, name='add_panel'),
    path('add_filetype/', filetype, name='add_filetype'),
    path('show_experiment', show_experiment, name='show_experiment'),
    path('show_experimentfile/', show_experimentfile, name='show_experimentfile'),
    path('add_experimentfile/', experimentfile.as_view(), name='add_experimentfile'),
]