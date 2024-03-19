from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import reverse_lazy

app_name = 'populateDB'

urlpatterns = [
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('home/', views.home, name='home'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(success_url=reverse_lazy('populateDB:password_change_done'), template_name='users/password_change_form.html'), name='password_change'),
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
    path('add_experimentfile/update_files/add_channels/analysis_type/<analysis_id>', views.analysis_type, name='analysis_type'),
    path('add_experimentfile/update_files/add_channels/analysis_type/marker_settings_autobat/<analysis_id>', views.marker_settings_autobat, name='marker_settings_autobat'),
    path('add_experimentfile/update_files/add_channels/analysis_type/marker_settings_autograt/<analysis_id>', views.marker_settings_autograt, name='marker_settings_autograt'),

    path('add_experimentfile/update_files/add_channels/analysis_type/marker_settings_autobat/run_analysis_autobat/<analysis_id>', views.run_analysis_autobat, name='run_analysis_autobat'),
    path('add_experimentfile/update_files/add_channels/analysis_type/marker_settings_autograt/run_analysis_autograt/<analysis_id>', views.run_analysis_autograt, name='run_analysis_autograt'),


    path('analysis/', views.show_analysis, name='show_analysis'),
    path('analysis/list_files/<analysis_id>', views.list_files, name='list_files'),

    path('analysis/delete_alert/<analysisMarker_id>', views.delete_analysis_alert, name='delete_alert'),
    path('analysis/delete_alert/delete_analysis/<analysisMarker_id>', views.delete_analysis, name='delete_analysis'),
    path('analysis/show_channels/<analysis_id>', views.show_channels, name='show_channels'),
    path('analysis/list_thresholds/<analysisMarker_id>', views.list_thresholds, name='list_thresholds'),
    path('analysis/download_pdf/<analysisMarker_id>', views.download_pdf, name='download_pdf'),
    path('analysis/download_xlsx/<analysisMarker_id>', views.download_xlsx, name='download_xlsx'),
    path('analysis_report/', views.analysis_report, name='analysis_report'),
    path('analysis_report/show_channels/<analysis_id>', views.show_channels, name='show_channels'),
    path('analysis_report/view_plots/<result_id>', views.view_plots, name='view_plots'),
    path('analysis_report/view_plots/update_plots_symbol/<analysisMarker_id>', views.update_plots_symbol, name='update_plots_symbol'),
    path('analysis/re_analysis_alert', views.re_analysis_alert, name='re_analysis_alert'),
    path('analysis/run_re_analysis_all', views.run_re_analysis_all, name='run_re_analysis_all'),

    path('analysis/re_analysis_all', views.re_analysis_all, name='re_analysis_all'),
    path('analysis/results_to_CSV', views.results_to_CSV, name='results_to_CSV'),
    path('analysis/thresholds_to_CSV', views.thresholds_to_CSV, name='thresholds_to_CSV'),
    path('thresholds_report/', views.thresholds_report, name='thresholds_report'),
    path('analysis/analysis_error/<analysisMarker_id>', views.analysis_error, name='analysis_error'),
    path('analysis/analysis_info/<analysisMarker_id>', views.analysis_info, name='analysis_info'),
    path('research_questions/', views.research_questions, name='research_questions'),
    path('research_results/', views.research_results, name='research_results'),
    #path('results/', views.ListResults.as_view(), name = 'list_results'),
    path('ajax/bat_names', views.getBat_names, name = "getBat_names"),
    path('ajax/file_controls', views.getFile_controls, name = "getFile_controls"),
    path('ajax/panel_names', views.getPanel_names, name = "getPanel_names"),
    path('ajax/clinical_classes', views.getClinical_classes, name = "getClinical_classes"),
    path('ajax/responders', views.getResponders, name = "getResponders"),
    path('ajax/allergens', views.get_allergens, name = "get_allergens"),
    path('research_results/downloadResults_pdf/<files_ids>', views.downloadResults_pdf, name='downloadResults_pdf'),
    path('research_results/downloadResults_xlsx/<excel_name>', views.downloadResults_xlsx, name='downloadResults_xlsx'),
    path('research_results/show_channels/<analysis_id>', views.show_channels, name='show_channels'),
    path('files_data_CSV', views.files_data_CSV, name='files_data_CSV'),
    path('blood_tests/', views.blood_tests, name='blood_tests'),
    path('skin_tests/', views.skin_tests, name='skin_tests'),
    path('ofc_tests/', views.ofc_tests, name='ofc_tests'),
    ]
