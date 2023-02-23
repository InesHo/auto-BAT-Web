from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)

app_name = 'populateDB'

urlpatterns = [
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('home/', views.home, name='home'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view( template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),    
    path('add_experiment/', views.add_experiment, name='add_experiment'),
    path('show_experiment', views.show_experiment, name='show_experiment'),
    path('add_experimenter/', views.add_experimenter, name='add_experimenter'),
    path('show_experimenter', views.show_experimenter, name='show_experimenter'),
    path('add_institute/', views.add_institute, name='add_institute'),
    path('show_institute', views.show_institute, name='show_institute'),
    path('add_department/', views.add_department, name='add_department'),
    path('show_department/', views.show_department, name='show_department'),
    path('add_device/', views.add_device, name='add_device'),
    path('show_device/', views.show_device, name='show_device'),
    path('add_donor/', views.add_donor, name='add_donor'),
    path('show_donor/', views.show_donor, name='show_donor'),
    path('add_panel/', views.add_panel, name='add_panel'),
    path('show_panel', views.show_panel, name='show_panel'),

    path('show_experimentfile/', views.show_experimentfile, name='show_experimentfile'),
    path('add_experimentfile/', views.experimentfile.as_view(), name='add_experimentfile'),
    path('show_experimentfile/show_metadata/<int:file_id>', views.show_metadata, name='show_metadata'),
    path('show_experimentfile/show_rawdata/<int:file_id>', views.show_rawMeanData, name='show_rawdata'),
    path('add_experimentfile/update_files/<analysis_id>', views.update_files, name='update_files'),
    path('add_experimentfile/update_files/add_channels/<analysis_id>', views.add_channels, name='add_channels'),
    path('add_experimentfile/update_files/add_channels/marker_settings/<analysis_id>', views.marker_settings, name='marker_settings'),
    path('add_experimentfile/update_files/add_channels/marker_settings/run_analysis/<analysis_id>', views.run_analysis, name='run_analysis'),

    path('analysis/', views.show_analysis, name='show_analysis'),
    path('analysis/list_files/<analysis_id>', views.list_files, name='list_files'),

    path('analysis/delete_alert/<analysisMarker_id>', views.delete_analysis_alert, name='delete_alert'),
    path('analysis/delete_alert/delete_analysis/<analysisMarker_id>', views.delete_analysis, name='delete_analysis'),
    path('analysis/show_channels/<analysis_id>', views.show_channels, name='show_channels'),
    path('analysis/download_pdf/<analysisMarker_id>', views.download_pdf, name='download_pdf'),
    path('analysis/download_xlsx/<analysisMarker_id>', views.download_xlsx, name='download_xlsx'),
    path('analysis_report/', views.analysis_report, name='analysis_report'),
    path('analysis_report/show_channels/<analysis_id>', views.show_channels, name='show_channels'),
    ]
