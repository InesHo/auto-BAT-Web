from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.views.generic import View
from django.http import HttpResponse, Http404
import sys
import os
from django.forms import formset_factory
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Case, When, Value, Count, Avg, Sum
from datetime import date
import config
sys.path.insert(0, os.path.join(config.AUTOBAT_PATH, 'autoBat'))
from django.conf import settings
from Data import Data
from .functions import create_path, image_grid, pdf_grid
from .tasks import run_analysis_autobat_task, run_analysis_autograt_task, proccess_files
from djqscsv import render_to_csv_response
from .serializers import ResultsSerializers
from .pagination import StandardResultsSetPagination
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
import pandas as pd
import time
import shutil
from django.db.models import F
import re
import csv

bat_version='1.0.3'
#'1.0.2'
grat_version='1.0.3'
#'1.0.1'

@login_required
def home(request):
    num_bats = models.Experiment.objects.all().count()
    num_donors = models.Donor.objects.all().count()
    num_files = models.ExperimentFiles.objects.all().count()
    num_analysis = models.AnalysisMarkers.objects.all().count()
    context = {
        "welcome": "Welcome to The Auto-Bat Web",
        'num_bats': num_bats,
        'num_donors': num_donors,
        'num_files': num_files,
        'num_analysis': num_analysis
    }
    return render(request, 'home.html', context=context)

@login_required
def add_user(request):
    if request.method == 'POST':
        form = forms.AddUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'users/add_user_done.html')
    else:
        form = forms.AddUserForm()

    context = {
        "form": form
    }
    return render(request, 'users/add_user.html', context=context)


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = forms.EditUserForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'users/edit_user_done.html')
    else:
        user_form = forms.EditUserForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'users/edit_user.html', context=context)

@login_required
def add_experiment(request):
    if request.method == 'POST':
        form = forms.ExperimentForm(request.POST or None)
        if form.is_valid():
            new_experiment = form.save(commit=False)
            new_experiment.save()
            experiment_data = models.Experiment.objects.all().order_by('bat_id').reverse()
            return render(request,"expermiments/show_experiment.html",{'experiment_data':experiment_data})
    else:
        form = forms.ExperimentForm()
    context = {
        "form": form
    }
    
    return render(request, 'expermiments/add_experiment.html', context=context)

@login_required
def show_experiment(request):  
    experiment_data = models.Experiment.objects.all().order_by('bat_id').reverse()
    return render(request,"expermiments/show_experiment.html",{'experiment_data':experiment_data})  

@login_required
def add_institute(request):
    institutes_data = models.Institutes.objects.all().order_by('institute_id').reverse()
    if request.method == 'POST':
        form = forms.InstitutesForm(request.POST or None)
        if form.is_valid():
            new_institute = form.save(commit=False)
            new_institute.save()            
            return render(request,"institutes/show_institutes.html",{'institutes_data':institutes_data}) 
    else:
        form = forms.InstitutesForm()

    context = {
        "form": form
    }

    return render(request, 'institutes/add_institutes.html', context=context)

@login_required
def show_institute(request):  
    institutes_data = models.Institutes.objects.all().order_by('institute_id').reverse()
    return render(request,"institutes/show_institutes.html",{'institutes_data':institutes_data}) 



@login_required
def add_panel(request):
    panels_data = models.Panels.objects.all().order_by('panel_id').reverse()
    if request.method == 'POST':
        form = forms.PanelsForm(request.POST or None)
        if form.is_valid():
            new_panel = form.save(commit=False)
            new_panel.save()
            return render(request,"panels/show_panels.html",{'panels_data':panels_data}) 
    else:
        form = forms.PanelsForm()

    context = {
        "form": form
    }

    return render(request, 'panels/add_panels.html', context=context)

@login_required
def show_panel(request):  
    panels_data = models.Panels.objects.all().order_by('panel_id').reverse()
    return render(request,"panels/show_panels.html",{'panels_data':panels_data}) 


@login_required
def add_department(request):
    departments_data = models.Departments.objects.all().order_by('department_id').reverse()
    if request.method == 'POST':
        form = forms.DepartmentsForm(request.POST or None)
        if form.is_valid():
            new_experiment = form.save(commit=False)
            new_experiment.save()
            return render(request,"departments/show_departments.html",{'departments_data':departments_data}) 
    else:
        form = forms.DepartmentsForm()
    context = {
        "form": form
    }
    return render(request, 'departments/add_departments.html', context=context)

@login_required
def show_department(request):  
    departments_data = models.Departments.objects.all().order_by('department_id').reverse()
    return render(request,"departments/show_departments.html",{'departments_data':departments_data}) 

@login_required
def add_experimenter(request):
    experimenters_data = models.Experimenters.objects.all().order_by('experimenter_id').reverse()
    if request.method == 'POST':
        form = forms.ExperimentersForm(request.POST or None)
        if form.is_valid():
            new_experimenter = form.save(commit=False)
            new_experimenter.save()
            return render(request,"experimenters/show_experimenters.html",{'experimenters_data':experimenters_data})
    else:
        form = forms.ExperimentersForm()

    context = {
        "form": form
    }
    return render(request, 'experimenters/add_experimenters.html', context=context)

@login_required
def show_experimenter(request):  
    experimenters_data = models.Experimenters.objects.all().order_by('experimenter_id').reverse()
    return render(request,"experimenters/show_experimenters.html",{'experimenters_data':experimenters_data})

@login_required
def add_device(request):
    devices_data = models.Devices.objects.all().order_by('device_id').reverse()
    if request.method == 'POST':
        form = forms.DevicesForm(request.POST or None)
        if form.is_valid():
            new_device = form.save(commit=False)
            new_device.save()
            return render(request,"devices/show_devices.html",{'devices_data':devices_data})
    else:
        form = forms.DevicesForm()

    context = {
        "form": form
    }
    return render(request, 'devices/add_devices.html', context=context)

@login_required
def show_device(request):  
    devices_data = models.Devices.objects.all().order_by('device_id').reverse()
    return render(request,"devices/show_devices.html",{'devices_data':devices_data})

@login_required
def add_donor(request):
    donors_data= models.Donor.objects.all().order_by('donor_id').reverse()
    if request.method == 'POST':
        form = forms.DonorForm(request.POST or None)
        if form.is_valid():
            new_donor = form.save(commit=False)
            new_donor.save()
            return render(request,"donors/show_donors.html",{'donors_data':donors_data})
    else:
        form = forms.DonorForm()

    context = {
        "form": form
    }
    return render(request, 'donors/add_donors.html', context=context)

@login_required
def show_donor(request):  
    donors_data= models.Donor.objects.all().order_by('donor_id').reverse()
    return render(request,"donors/show_donors.html",{'donors_data':donors_data})

class experimentfile(View):
    def get(self, request):
        form = forms.ExperimentFilesForm()
        return render(request, 'files/add_files.html', context={'form':form})

    def post(self, request):
        if request.method=='POST':
            form = forms.ExperimentFilesForm(request.POST, request.FILES)
            files = request.FILES.getlist('file')
            if form.is_valid():
                bat_id = form.cleaned_data['bat_id']
                donor_id = form.cleaned_data['donor_id']
                panel_id = form.cleaned_data['panel_id']
                condition = form.cleaned_data['condition']
                condition = condition.replace(" ", "_")
                analysis_instance = models.Analysis(bat_id=bat_id, donor_id=donor_id, panel_id=panel_id, condition=condition)
                analysis_instance.user_id = request.user.id
                analysis_instance.save()
                analysis_id = analysis_instance.analysis_id
                if condition:
                    files_dir = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_id}/{donor_id}/{panel_id}/{condition}")
                else:
                    files_dir = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_id}/{donor_id}/{panel_id}")
                create_path(files_dir)
                file_list = []
                us_file_path = ""
                for f in files:
                    fs = FileSystemStorage(files_dir)           
                    file_path = fs.save(f.name, f)  
                    file_path = os.path.join(files_dir, str(file_path))
                    dataO = Data(filetype="FCS", filename = file_path)
                    data = dataO.getData()
                    meta = data.get_metadata()
                    allergen = meta.get('cells')
                    if allergen is not None:
                        if '_' in allergen:
                            allergen = allergen.split("_")
                            allergen = allergen[-1]
                    
                    control = "Allergen"
                    file_instance = models.ExperimentFiles(file_name = f, file=file_path, allergen=allergen, control=control)
                    file_instance.analysis_id_id = int(analysis_id)
                    file_instance.user_id = request.user.id
                    file_instance.save()
                    
                    us_file_path = file_path

                dataO = Data(filetype="FCS", filename = us_file_path)
                data = dataO.getData()
                channels = data.channels
                for i in range(1, len(channels) + 1):
                    c = channels[str(i)]
                    pnn = c['PnN']
                    if len(c) == 1:
                        c['PnS'] = pnn

                    pns = c['PnS']
                    channel_obj = models.Channels(
                                                pnn = pnn,
                                                pns = pns,
                                                )
                    channel_obj.analysis_id_id = int(analysis_id)
                    channel_obj.save()

                proccess_files(analysis_id, repeat=0)

                return render(request, 'files/files_ready.html', {'analysis_id':analysis_id})
            else:
                return render(request, 'files/files_error.html')


@login_required
def show_experimentfile(request):  
    file_data = models.ExperimentFiles.objects.all().order_by('file_id').reverse()
    return render(request,"files/show_files.html",{'file_data':file_data})

@login_required
def show_metadata(request, file_id):  
    meta_data = models.MetaData.objects.filter(file_id = file_id)
    return render(request,"files/show_metadata.html",{'meta_data':meta_data})

@login_required
def show_rawMeanData(request, file_id):  
    mean_data = models.MeanRawData.objects.filter(file_id = file_id)
    return render(request,"files/show_meandata.html",{'mean_data':mean_data})

@login_required
def update_files(request, analysis_id):
    files_list = []
    files = models.ExperimentFiles.objects.filter(analysis_id=analysis_id)
    for file in files:
        file_dict={}
        file_dict['file_id'] = file.file_id
        file_dict['file_name'] = file.file_name
        file_dict['allergen'] = file.allergen
        file_dict['control'] = file.control
        file_dict['analysis_id'] = file.analysis_id
        files_list.append(file_dict)
    FilesFormset = formset_factory(forms.UpdateFilesForm)
    if request.method == 'POST':
        formset = FilesFormset(request.POST or None, request.FILES, initial=files_list)
        if formset.is_valid():
            negative_control = ''
            for form in formset[:-1]:
                file_id = form.cleaned_data['file_id']
                allergen = form.cleaned_data['allergen']
                control = form.cleaned_data['control']
                models.ExperimentFiles.objects.filter(file_id=file_id).update(allergen=allergen)
                models.ExperimentFiles.objects.filter(file_id=file_id).update(control=control)
                
                if control == "Negative control":
                    negative_control = file_id
                """
                    file_path = get_object_or_404(models.ExperimentFiles.objects.filter(file_id=negative_control).values_list('file', flat=True))
                    dataO = Data(filetype="FCS", filename = file_path)
                    data = dataO.getData()
                    channels = data.channels
                    for i in range(1, len(channels) + 1):
                        c = channels[str(i)]
                        pnn = c['PnN']
                        if len(c) == 1:
                            c['PnS'] = pnn

                        pns = c['PnS']
                        channel_obj = models.Channels(
                                                pnn = pnn,
                                                pns = pns,
                                                )
                        channel_obj.analysis_id_id = int(analysis_id)
                        channel_obj.save()
                """
            if negative_control:
                return render(request, 'files/filesUpdate_ready.html', {'analysis_id': analysis_id})
            else:
                return render(request, 'files/filesUpdate_error.html', {'analysis_id': analysis_id})
    else:
        formset = FilesFormset(initial=files_list)
    return render(request, 'files/update_files.html', {'formset': formset})

@login_required()
def add_channels(request, analysis_id):  

    channel_list = []
    channels = models.Channels.objects.filter(analysis_id=analysis_id).order_by('channel_id')

    for channel in channels:
        channel_dict={}
        channel_dict['channel_id'] = channel.channel_id
        channel_dict['pnn'] = channel.pnn
        channel_dict['pns'] = channel.pns
        channel_dict['analysis_id'] = channel.analysis_id
        channel_list.append(channel_dict)
    
    ChannelsFormset = formset_factory(forms.ChannelsForm)
    if request.method == 'POST':
        formset = ChannelsFormset(request.POST or None, request.FILES, initial=channel_list)
        if formset.is_valid():
            for form in formset[:-1]:                
                channel_id = form.cleaned_data['channel_id']
                pns = form.cleaned_data['pns']
                models.Channels.objects.filter(channel_id=channel_id).update(pns=pns)
            return render(request, 'channels/panels_ready.html', {'analysis_id': analysis_id})     
    else:
        formset = ChannelsFormset(initial=channel_list)
    return render(request, 'channels/add_channels.html', {'formset': formset})

@login_required
def show_channels(request, analysis_id):  
    channels_data = models.Channels.objects.filter(analysis_id=analysis_id)
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

    return render(request,"channels/show_channels.html",{'channels_data':channels_data, 'bat_name': bat_name, 'donor_name': donor_name, 'panel_name': panel_name})

def marker_settings_autobat(request, analysis_id): 
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))

    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))


    channels = models.Channels.objects.filter(pnn__endswith=("A") ,analysis_id = analysis_id).order_by('channel_id')
    return render(request, 'analysis/marker_settings_autobat.html', {'channels': channels, 'analysis_id': analysis_id, 'bat_name':bat_name, 'donor_name':donor_name, 'panel_name':panel_name}) 


def marker_settings_autograt(request, analysis_id):
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))

    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))


    channels = models.Channels.objects.filter(pnn__endswith=("A") ,analysis_id = analysis_id).order_by('channel_id')
    return render(request, 'analysis/marker_settings_autograt.html', {'channels': channels, 'analysis_id': analysis_id, 'bat_name':bat_name, 'donor_name':donor_name, 'panel_name':panel_name})


@login_required
def analysis_type(request, analysis_id):
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))

    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

    if request.method == "POST":
        if request.POST.get('analysis_type') == "auto_bat":
            return render(request, 'analysis/marker_settings_autobat.html', {'analysis_id': analysis_id})
        if request.POST.get('analysis_type') == "auto_grat":
            return render(request, 'analysis/marker_settings_autograt.html', {'analysis_id': analysis_id})
    return render(request, 'analysis/choose_analysis_type.html', {'analysis_id':analysis_id, 'bat_name':bat_name, 'donor_name':donor_name, 'panel_name':panel_name})

@login_required
def run_analysis_autobat(request, analysis_id):

    if request.method == "POST":

        bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
        donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
        panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
        
        condition = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('condition', flat=True))

        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        # for Manual Thresholds:
        xMarkerThreshhold = request.POST.get('xMarkerThreshhold')
        yMarkerThreshold = request.POST.get('yMarkerThreshold')
        z1MarkerThreshold = request.POST.get('z1MarkerThreshold')
        manualThresholds = request.POST.get('manualThresholds')
        if manualThresholds == 'Yes':
            manualThresholds = True
        else:
            manualThresholds = False

        chosen_z1 = request.POST.get('z1')
        chosen_z1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z1).values_list('pns', flat=True))
        chosen_y1 = request.POST.get('y1')
        chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))
        chosen_z2 = request.POST.get('z2')
        analysis_date = str(date.today())
        analysis_status = "Waiting"
        analysis_type = "AutoBat"
        analysis_type_version = bat_version
        user_id = request.user.id

        # Checking if the Experment has alrady been Analyzed with those markers
        analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                chosen_z1 = chosen_z1,
                                                chosen_y1=chosen_y1,
                                                chosen_z2=chosen_z2,
                                                analysis_type=analysis_type,
                                                analysis_type_version = analysis_type_version,
                                                analysis_id = analysis_id)
        if not analysismarkers_data:

            analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_z1,
                                                        chosen_y1=chosen_y1,
                                                        chosen_z2=chosen_z2,
                                                        analysis_date=analysis_date,
                                                        analysis_status=analysis_status,
                                                        analysis_type=analysis_type,
                                                        analysis_type_version = analysis_type_version,
                                                        analysis_manualThresholds=manualThresholds,
                                                        )
            analysismarkers_instance.analysis_id_id = int(analysis_id)
            analysismarkers_instance.user_id = user_id
            analysismarkers_instance.save()
            
            analysisMarker_id = analysismarkers_instance.analysisMarker_id


            device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
            device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))
            
            outputPDFname = f"Autobat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}_{analysis_type_version}.png"
            pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/") 
            pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/AutoBat/")       
            create_path(pathToExports)
            pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autobat/{analysis_type_version}/")
            create_path(pathToOutput)
            pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
            rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
            run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_z1_lable, chosen_y1,
                                chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports, 
                                pathToOutput, pathToGatingFunctions, rPath, manualThresholds, xMarkerThreshhold, yMarkerThreshold, z1MarkerThreshold, analysis_type_version, user_id
                                )
            return render(request, 'analysis/analysis_ready.html')
        else:
            return render(request, 'analysis/analysis_error.html', {'analysis_id':analysis_id})

@login_required
def run_analysis_autograt(request, analysis_id):

    if request.method == "POST":

        bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
        donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
        panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
        
        condition = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('condition', flat=True))

        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        chosen_x = request.POST.get('X')
        chosen_x_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_x).values_list('pns', flat=True))
        chosen_y1 = request.POST.get('Y')
        chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))
        chosen_z2_1 = request.POST.get('Z2_1')
        chosen_z2_2 = request.POST.get('Z2_2')
        chosen_z2_3 = request.POST.get('Z2_3')
        chosen_z2_4 = request.POST.get('Z2_4')
        if chosen_z2_1 =="None":
            chosen_z2_1 = None
        if chosen_z2_2 =="None":
            chosen_z2_2 = None
        if chosen_z2_3 =="None":
            chosen_z2_3 = None
        if chosen_z2_4 =="None":
            chosen_z2_4 = None
    
        chosen_z2 = list()
        chosen_z2.append(chosen_z2_1)
        chosen_z2.append(chosen_z2_2)
        chosen_z2.append(chosen_z2_3)
        chosen_z2.append(chosen_z2_4)
        if chosen_z2_1:
            chosen_z2_1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_1).values_list('pns', flat=True))
        else:
            chosen_z2_1_lable = None
        if chosen_z2_2:
            chosen_z2_2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_2).values_list('pns', flat=True))
        else:
            chosen_z2_2_lable = None
        if chosen_z2_3:
            chosen_z2_3_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_3).values_list('pns', flat=True))
        else:
            chosen_z2_3_lable = None
        if chosen_z2_4:
            chosen_z2_4_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_4).values_list('pns', flat=True))
        else:
            chosen_z2_4_lable = None
        chosen_z2_lable = list()
        chosen_z2_lable.append(chosen_z2_1_lable)
        chosen_z2_lable.append(chosen_z2_2_lable)
        chosen_z2_lable.append(chosen_z2_3_lable)
        chosen_z2_lable.append(chosen_z2_4_lable)
        analysis_date = str(date.today())
        chosen_z1 = "FSC-A"
        chosen_z1_lable = "FSC_A"
        analysis_status = "Waiting"
        analysis_type = "AutoGrat"
        analysis_type_version = grat_version
        user_id = request.user.id
        

        if any(chosen_z2):
            # Checking if the Experment has alrady been Analyzed with the selected markers
            analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                chosen_z1 = chosen_x,
                                                chosen_y1=chosen_y1,
                                                chosen_z2=chosen_z2_1,
                                                chosen_z2_2=chosen_z2_2,
                                                analysis_type=analysis_type,
                                                analysis_type_version = analysis_type_version,
                                                analysis_id = analysis_id) 
            if not analysismarkers_data:

                analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_x,
                                                        chosen_y1=chosen_y1,
                                                        chosen_z2=chosen_z2,
                                                        analysis_date=analysis_date,
                                                        analysis_status=analysis_status,
                                                        analysis_type=analysis_type,
                                                        analysis_type_version = analysis_type_version,
                                                        )
                analysismarkers_instance.analysis_id_id = int(analysis_id)
                analysismarkers_instance.user_id = user_id
                analysismarkers_instance.save()
            
                analysisMarker_id = analysismarkers_instance.analysisMarker_id

                
                device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
                device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))
            
                outputPDFname = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_x}_{chosen_y1}_{chosen_z2}_{analysis_type_version}.png"
                pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/") 
                pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/AutoGrat/")       
                create_path(pathToExports)
                pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autograt/{analysis_type_version}/")
                create_path(pathToOutput)
                pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
                rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
                run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_x, chosen_x_lable, chosen_y1, chosen_y1_lable, chosen_z1, chosen_z1_lable,
                                chosen_z2, chosen_z2_lable, device, outputPDFname, pathToData, pathToExports, pathToOutput, pathToGatingFunctions, rPath, analysis_type_version, user_id
                                )
                return render(request, 'analysis/analysis_ready.html')
            else:
                return render(request, 'analysis/analysis_error.html', {'analysis_id':analysis_id})
        else:
            return render(request, 'analysis/analysis_markers_error.html', {'analysis_id':analysis_id})
@login_required
def results_to_CSV(request):
    analysisResults = models.AnalysisResults.objects.values('analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_type',
                                                            'analysisMarker_id__analysis_id__condition',
                                                            'analysisMarker_id__analysis_type_version',
                                                            'file_id__file_name', 
                                                            #"analysisMarker_id__analysis_error", 
                                                            "analysisMarker_id__analysis_info_messages",
                                                            'redQ4', 'result', 'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4', 'msi_YQ4', 'cellQ4', 'responder')
    return render_to_csv_response(analysisResults)

@login_required
def thresholds_to_CSV(request):
    thresholds = models.AnalysisThresholds.objects.values('analysisMarker_id__analysis_id__bat_id__bat_name','analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name', 'analysisMarker_id__analysis_id__condition',
                                                            'analysisMarker_id__analysis_type','analysisMarker_id__analysis_type_version', 
                                                            'X_Threshold', 'Y_Threshold', 'Z2_1_Threshold', 'Z2_2_Threshold',
                                                            #"analysisMarker_id__analysis_error",
                                                            "analysisMarker_id__analysis_info_messages"
                                                            )
    return render_to_csv_response(thresholds)


@login_required
def re_analysis_all(request):
    user_id = request.user.id
    #bat_version
    #grat_version
    if request.method == "POST":

        analysis_type = request.POST.get('analysis_type')

        if  analysis_type == 'AutoBat':
            analysisMarker_obj = models.AnalysisMarkers.objects.values_list('analysisMarker_id', 'analysis_status').filter(analysis_type=analysis_type)
            for analysismarker in analysisMarker_obj:
                analysisMarker_id = analysismarker[0]
                current_version = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type_version', flat=True))
                analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
            #analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))
                bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
                donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
                panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
                bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
                donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
                panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

                condition = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('condition', flat=True))

                chosen_z1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z1', flat=True))
                chosen_y1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_y1', flat=True))
                chosen_z2 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z2', flat=True))
            #chosen_z2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2).values_list('pns', flat=True))
                chosen_z1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z1).values_list('pns', flat=True))
                chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))

                device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
                device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))
                pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/")
                pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
                rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
                manualThresholds = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_manualThresholds', flat=True))
                if manualThresholds == 'Yes':
                    xMarkerThreshhold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('X_Threshold', flat=True))
                    yMarkerThreshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Y_Threshold', flat=True))
                    z1MarkerThreshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Z2_1_Threshold', flat=True))
                else:
                    xMarkerThreshhold = 0
                    yMarkerThreshold = 0
                    z1MarkerThreshold = 0
                
                analysis_type_version = bat_version
                chosen_z2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2).values_list('pns', flat=True))
                outputPDFname = f"AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}_{bat_version}.png"
                pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/AutoBat/")
                create_path(pathToExports)
                pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autobat/{bat_version}/")
                create_path(pathToOutput)

                if current_version == bat_version:
                    models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.FilesPlots.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisResults.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Waiting")
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_error="")
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages="")
                    run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_z1_lable, chosen_y1,
                                                chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports,
                                                pathToOutput, pathToGatingFunctions, rPath, manualThresholds, xMarkerThreshhold, yMarkerThreshold, z1MarkerThreshold, analysis_type_version, user_id
                                        )
                else:
                    analysis_date = str(date.today())
                    analysis_status = "Waiting"
                    analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(chosen_z1 = chosen_z1,
                                                                                        chosen_y1=chosen_y1,
                                                                                        chosen_z2=chosen_z2,
                                                                                        analysis_type=analysis_type,
                                                                                        analysis_type_version = analysis_type_version,
                                                                                        analysis_id = analysis_id)
                    if not analysismarkers_data:

                        analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_z1,
                                                                    chosen_y1=chosen_y1,
                                                                    chosen_z2=chosen_z2,
                                                                    analysis_date=analysis_date,
                                                                    analysis_status=analysis_status,
                                                                    analysis_type=analysis_type,
                                                                    analysis_type_version = analysis_type_version,
                                                                    analysis_manualThresholds=manualThresholds,
                                                                )
                        analysismarkers_instance.analysis_id_id = int(analysis_id)
                        analysismarkers_instance.user_id = user_id
                        analysismarkers_instance.save()
                        analysisMarker_id = analysismarkers_instance.analysisMarker_id
                        run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_z1_lable, chosen_y1,
                                chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports,
                                pathToOutput, pathToGatingFunctions, rPath, manualThresholds, xMarkerThreshhold, yMarkerThreshold, z1MarkerThreshold, analysis_type_version, user_id
                                )
            return render(request, 'analysis/analysis_ready.html')
        elif analysis_type == 'AutoGrat':
            analysisMarker_obj = models.AnalysisMarkers.objects.values_list('analysisMarker_id', 'analysis_status').filter(analysis_type=analysis_type)
            
            for analysismarker in analysisMarker_obj:
                analysisMarker_id = analysismarker[0]
                current_version = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type_version', flat=True))
                analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
            #analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))
                bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
                donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
                panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
                bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
                donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
                panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

                chosen_z1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z1', flat=True))
                chosen_y1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_y1', flat=True))
                chosen_z2 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z2', flat=True))
            #chosen_z2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2).values_list('pns', flat=True))
                chosen_z1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z1).values_list('pns', flat=True))
                chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))

                device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
                device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))
                pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/")
                pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
                rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
                manualThresholds = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_manualThresholds', flat=True))
                if manualThresholds == 'Yes':
                    xMarkerThreshhold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('X_Threshold', flat=True))
                    yMarkerThreshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Y_Threshold', flat=True))
                    z1MarkerThreshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Z2_1_Threshold', flat=True))

                analysis_type_version = grat_version
                chosen_x = chosen_z1
                chosen_x_lable = chosen_z1_lable
                chosen_z1 = "FSC-A"
                chosen_z1_lable = "FSC_A"
                
                chosen_z2 = re.sub("[][',]", '', chosen_z2)
                chosen_z2 = chosen_z2.split()
                
                chosen_z2_1 = chosen_z2[0] 
                chosen_z2_2 = chosen_z2[1]
                chosen_z2_3 = chosen_z2[2]
                chosen_z2_4 = chosen_z2[3]

                if chosen_z2_1 == "None":
                    chosen_z2_1 = None
                    chosen_z2_1_lable = None
                else:
                    chosen_z2_1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_1).values_list('pns', flat=True))
                
                if chosen_z2_2 == "None":
                    chosen_z2_2 = None
                    chosen_z2_2_lable = None
                else:
                    chosen_z2_2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_2).values_list('pns', flat=True))
            
                if chosen_z2_3 == "None":
                    chosen_z2_3 = None
                    chosen_z2_3_lable = None
                else:
                    chosen_z2_3_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_3).values_list('pns', flat=True))
                
                if chosen_z2_4 == "None":
                    chosen_z2_4 = None
                    chosen_z2_4_lable = None
                else:
                    chosen_z2_4_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2_4).values_list('pns', flat=True))
                
                chosen_z2_list = list()
                chosen_z2_list.append(chosen_z2_1)
                chosen_z2_list.append(chosen_z2_2)
                chosen_z2_list.append(chosen_z2_3)
                chosen_z2_list.append(chosen_z2_4)

                chosen_z2_lable_list = list()
                chosen_z2_lable_list.append(chosen_z2_1_lable)
                chosen_z2_lable_list.append(chosen_z2_2_lable)
                chosen_z2_lable_list.append(chosen_z2_3_lable)
                chosen_z2_lable_list.append(chosen_z2_4_lable)

                

                pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/AutoGrat/")
                create_path(pathToExports)
                outputPDFname = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}_{grat_version}.png"
                pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autograt/{grat_version}/")
                create_path(pathToOutput)
            
                if current_version == grat_version:
                    models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.FilesPlots.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisResults.objects.filter(analysisMarker_id=analysisMarker_id).delete()
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Waiting")
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_error="")
                    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_info_messages="")
                    run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_x, chosen_x_lable, chosen_y1, chosen_y1_lable, chosen_z1, 
                                                chosen_z1_lable, chosen_z2_list, chosen_z2_lable_list, device, outputPDFname, pathToData, pathToExports, pathToOutput, 
                                                pathToGatingFunctions, rPath, analysis_type_version, user_id )
                else:
                    analysis_date = str(date.today())
                    analysis_status = "Waiting"
                    analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                                        chosen_z1 = chosen_x,
                                                                        chosen_y1=chosen_y1,
                                                                        chosen_z2=chosen_z2_list,
                                                                        analysis_type=analysis_type,
                                                                        analysis_type_version = analysis_type_version,
                                                                        analysis_id = analysis_id)
                    if not analysismarkers_data:
                        analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_x,
                                                                    chosen_y1=chosen_y1,
                                                                    chosen_z2=chosen_z2_list,
                                                                    analysis_date=analysis_date,
                                                                    analysis_status=analysis_status,
                                                                    analysis_type=analysis_type,
                                                                    analysis_type_version = analysis_type_version,
                                                                    analysis_manualThresholds=manualThresholds)
                        analysismarkers_instance.analysis_id_id = int(analysis_id)
                        analysismarkers_instance.user_id = user_id
                        analysismarkers_instance.save()
                        analysisMarker_id = analysismarkers_instance.analysisMarker_id
            
                        run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_x, chosen_x_lable, chosen_y1, chosen_y1_lable, chosen_z1,
                                                    chosen_z1_lable, chosen_z2_list, chosen_z2_lable_list, device, outputPDFname, pathToData, pathToExports, pathToOutput, 
                                                    pathToGatingFunctions, rPath, analysis_type_version, user_id)
            return render(request, 'analysis/analysis_ready.html')
        else:
            return render(request, 'analysis/re_analysis_error.html')

@login_required()
def show_analysis(request):
    user_is_superuser = request.user.is_superuser
    analysis = models.Analysis.objects.values_list('analysis_id', 'bat_id','donor_id', 'panel_id', 'condition').order_by('bat_id').reverse()
    analysisList = []
    for i in analysis:
        analysis_id = i[0]
        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=i[1]).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=i[2]).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=i[3]).values_list('panel_name', flat=True))       
        condition = i[4]
        analysismarkers = models.AnalysisMarkers.objects.values_list('analysisMarker_id', 
                                                    'chosen_z1', 'chosen_y1','chosen_z2', 'chosen_z2_2', 'analysis_date',
                                                    'analysis_start_time', 'analysis_end_time','analysis_status', 'analysis_type', 'analysis_type_version',
                                                    'analysis_manualThresholds', 'analysis_info_messages'
                                                    ).filter(analysis_id = analysis_id).order_by('analysisMarker_id').reverse()
    


        if not analysismarkers:
            analysis_dict = {}
            analysis_dict['analysis_id'] = analysis_id
            analysis_dict['bat_name'] = bat_name
            analysis_dict['donor_name'] = donor_name
            analysis_dict['panel_name'] = panel_name
            analysis_dict['condition'] = condition
            analysis_dict['analysisMarker_id'] = None
            analysis_dict['chosen_z1'] = None
            analysis_dict['chosen_y1'] = None
            analysis_dict['chosen_z2'] = None
            analysis_dict['chosen_z2_2'] = None
            analysis_dict['analysis_date'] = None
            analysis_dict['analysis_start_time'] = None
            analysis_dict['analysis_end_time'] = None
            analysis_dict['analysis_status'] = None
            analysis_dict['analysis_type'] = None
            analysis_dict['analysis_type_version'] = None
            analysisList.append(analysis_dict)
        else:
        
            for j in analysismarkers:
                analysis_dict = {}
                analysis_dict['analysis_id'] = analysis_id
                analysis_dict['bat_name'] = bat_name
                analysis_dict['donor_name'] = donor_name
                analysis_dict['panel_name'] = panel_name
                analysis_dict['condition'] = condition
                analysis_dict['analysisMarker_id'] = j[0]
                analysis_dict['analysis_info_messages'] = j[11]
                if j[11] == '[]' or j[11] == '' or j[11] == None:
                    analysis_dict['info'] = 'No'
                else:
                    analysis_dict['info'] = 'Yes'
                analysis_dict['chosen_z1'] = j[1]
                analysis_dict['chosen_y1'] = j[2]
                analysis_dict['chosen_z2'] = j[3]
                analysis_dict['chosen_z2_2'] = j[4]
                analysis_dict['analysis_date'] = j[5]
                analysis_dict['analysis_start_time'] = j[6]
                analysis_dict['analysis_end_time'] = j[7]
                analysis_dict['analysis_status'] = j[8]
                analysis_dict['analysis_type'] = j[9]
                analysis_dict['analysis_type_version'] = j[10]
                analysis_dict['analysis_manualThresholds'] = j[11]
                analysisList.append(analysis_dict)
    return render(request, 'analysis/analysis_list.html',{'analysis':analysisList, 'user_is_superuser':user_is_superuser})


@login_required
def delete_analysis_alert(request, analysisMarker_id):
    analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))
    return render(request, 'analysis/analysis_delete_alert.html', {'analysisMarker_id':analysisMarker_id, 'bat_name': bat_name, 'donor_name': donor_name, 'panel_name': panel_name})


@login_required
def re_analysis_alert(request):
    return render(request, 'analysis/re_analysis_alert.html')

@login_required
def run_re_analysis_all(request):
        return render(request, 'analysis/re_analysis_all.html')

@login_required
def list_files(request, analysis_id):  
    files_list = models.ExperimentFiles.objects.filter(analysis_id=analysis_id)
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

    return render(request,"files/list_files.html",{'files_list':files_list, 'bat_name': bat_name, 'donor_name': donor_name, 'panel_name': panel_name})

@login_required
def list_thresholds(request, analysisMarker_id):
    X_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('X_Threshold', flat=True))
    Y_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Y_Threshold', flat=True))
    Z2_1_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Z2_1_Threshold', flat=True))
    Z2_2_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('Z2_2_Threshold', flat=True))
    analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))
    analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))

    return render(request,"analysis/list_thresholds.html",{'X_Threshold':X_Threshold,'Y_Threshold':Y_Threshold,'Z2_1_Threshold':Z2_1_Threshold,
                                                           'Z2_2_Threshold':Z2_2_Threshold,'bat_name': bat_name,'donor_name': donor_name, 'panel_name': panel_name,
                                                           'analysis_type': analysis_type})


@login_required
def delete_analysis(request, analysisMarker_id):
    analysisMarker_id = analysisMarker_id
    models.FilesPlots.objects.filter(analysisMarker_id=analysisMarker_id).delete()
    models.AnalysisResults.objects.filter(analysisMarker_id=analysisMarker_id).delete()
    models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
    models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).delete()
    models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()

    return render(request, 'analysis/analysis_deleted.html')


@login_required
def download_pdf(request, analysisMarker_id):
    file_path = get_object_or_404(models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id, file_type = 'PDF').values_list('file_path', flat=True))
    if os.path.exists(str(file_path)):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def download_xlsx(request, analysisMarker_id):
    file_path = get_object_or_404(models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id, file_type = 'Excel').values_list('file_path', flat=True))
    if os.path.exists(str(file_path)):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def analysis_report(request):
    analysisResults = models.AnalysisResults.objects.values('analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_id__condition',
                                                            'analysisMarker_id__analysis_type',
                                                            'analysisMarker_id__analysis_type_version',
                                                            'file_id__file_name', 'file_id__allergen','file_id__control',
                                                            'zMarker', 'debrisPerc', 'firstDoubPerc', 'secDoubPerc', 'redQ4', 'result',
                                                            'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4',
                                                            'msi_YQ4', 'cellQ3', 'cellQ4', 'responder', 'cellTotal', 'qualityMessages', 'plot_symbol'
                                                            ).annotate(
                                                                Analysis_Type=F('analysisMarker_id__analysis_type'),
                                                                Analysis_Version=F('analysisMarker_id__analysis_type_version')
                                                            ).filter(Analysis_Version=Case(
                                                                                            When(Analysis_Type='AutoBat', then=Value(bat_version)),
                                                                                            When(Analysis_Type='AutoGrat', then=Value(grat_version))
                                                                                            )
                                                                    )

    return render(request,"analysis/analysis_report.html",{'analysis_results':analysisResults})

@login_required
def thresholds_report(request):


    analysisThresholds = models.AnalysisThresholds.objects.values('analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_id__condition',
                                                            'analysisMarker_id__analysis_type_version',
                                                            'analysisMarker_id__analysis_type',

                                                            'X_Threshold', 'Y_Threshold', 'Z2_1_Threshold', 'Z2_2_Threshold', 'analysisMarker_id__chosen_z1'
                                                            ,'analysisMarker_id__chosen_y1', 'analysisMarker_id__chosen_z2')

    return render(request,"analysis/analysis_thresholds.html",{'analysisThresholds': analysisThresholds})

@login_required
def analysis_error(request, analysisMarker_id):
    error = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_error', flat=True))
    analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))
    analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))

    return render(request,"analysis/show_error.html",{'error':error,  'bat_name': bat_name,'donor_name': donor_name, 'panel_name': panel_name,
                                                      'analysis_type': analysis_type})

@login_required
def analysis_info(request, analysisMarker_id):
    info_messages = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_info_messages', flat=True))
    analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))
    analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))
    return render(request,"analysis/show_info_messages.html",{'info_messages':info_messages, 'bat_name': bat_name,
                                                              'donor_name': donor_name, 'panel_name': panel_name, 'analysis_type': analysis_type})

@login_required
def blood_tests(request):
    test_results = models.DonorTestBlood.objects.values('donor_id__donor_abbr', 'gIgE', 'wheat_flour', 'gluten', 'gliadin', 'Tri_a_19', 'Tri_a_14', 'Tryptase',
                                                        'donor_id__donorclinicalclass__clinicalClass_id__clinicalClass_name')
    return render(request, "clinical_tests/blood_test.html", {"test_results": test_results})

@login_required
def skin_tests(request):
    test_results = models.DonorTest_SPT.objects.values('donor_id__donor_abbr', 'Histamine', 'NaCl', 'wheat_flour', 'wheat_gluten', 'birch', 'mugworth',  'timothy', 'house_dust_mite', 'cat',
                                                        'donor_id__donorclinicalclass__clinicalClass_id__clinicalClass_name')
    return render(request, "clinical_tests/skin_test.html", {"test_results": test_results})

@login_required
def ofc_tests(request):
    test_results = models.DonorTestOFC.objects.values('donor_id__donor_abbr', 'gram_limit_ofc', 'donor_ofc', 
                                                        'donor_id__donortestofc_exercise__gram_limit_ofc_exercise',
                                                        'donor_id__donortestofc_exercise__donor_ofc_exercise',
                                                        'donor_id__donorclinicalclass__clinicalClass_id__clinicalClass_name')
    return render(request, "clinical_tests/ofc_test.html", {"test_results": test_results})
######################################################################
#@login_required(login_url='/login/') #redirect when user is not logged in
def research_questions(request):
    return render(request, "analysis/research_questions.html")

def is_valid_queryparam(param):
    return param != '' and param is not None
def research_results(request):
    
    queryList = models.AnalysisResults.objects.values(      'id', 
                                                            'analysisMarker_id',
                                                            'analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_id__condition',
                                                            'analysisMarker_id__analysis_id__bat_id__date_of_measurement',
                                                            'analysisMarker_id__analysis_type',
                                                            'analysisMarker_id__analysis_type_version',
                                                            'file_id', 'file_id__file_name', 'file_id__allergen','file_id__control',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclinicalclass__clinicalClass_id__clinicalClass_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestofc__donor_ofc',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestofc__gram_limit_ofc',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestofc_exercise__donor_ofc_exercise',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestofc_exercise__gram_limit_ofc_exercise',

                                                            'zMarker', 'redQ4', 'result','blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4',
                                                            'msi_YQ4', 'cellQ3', 'cellQ4', 'responder', 'cellTotal',
                                                            
                                                            'analysisMarker_id__analysisthresholds__X_Threshold',
                                                            'analysisMarker_id__analysisthresholds__Y_Threshold',
                                                            'analysisMarker_id__analysisthresholds__Z2_1_Threshold',
                                                            'analysisMarker_id__analysisthresholds__Z2_2_Threshold',

                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__gIgE',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__wheat_flour',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__gluten',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__gliadin',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_19',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_14',
                                                            'analysisMarker_id__analysis_id__donor_id__donortestblood__Tryptase',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__Histamine',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__NaCl',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_flour',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_gluten',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__birch',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__mugworth',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__timothy',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__house_dust_mite',
                                                            'analysisMarker_id__analysis_id__donor_id__donortest_spt__cat',                         

                                                            ).annotate(
                                                                Analysis_id=F('analysisMarker_id__analysis_id'),
                                                                BAT_ID=F('analysisMarker_id__analysis_id__bat_id__bat_name'),
                                                                Donor=F('analysisMarker_id__analysis_id__donor_id__donor_abbr'),
                                                                Panel=F('analysisMarker_id__analysis_id__panel_id__panel_name'),
                                                                Condition=F('analysisMarker_id__analysis_id__condition'),
                                                                Date=F('analysisMarker_id__analysis_id__bat_id__date_of_measurement'),
                                                                Analysis_Type=F('analysisMarker_id__analysis_type'),
                                                                Analysis_Version = F('analysisMarker_id__analysis_type_version'),
                                                                File_Name = F('file_id__file_name'),
                                                                File_id = F('file_id'),
                                                                Allergen = F('file_id__allergen'),
                                                                Control = F('file_id__control'),
                                                                X_Threshold = F('analysisMarker_id__analysisthresholds__X_Threshold'),
                                                                Y_Threshold = F('analysisMarker_id__analysisthresholds__Y_Threshold'),
                                                                Z2_1_Threshold = F('analysisMarker_id__analysisthresholds__Z2_1_Threshold'),
                                                                Z2_2_Threshold = F('analysisMarker_id__analysisthresholds__Z2_2_Threshold'),
                                                                Clinical_class=F('analysisMarker_id__analysis_id__donor_id__donorclinicalclass__clinicalClass_id__clinicalClass_name'),
                                                                OFC_classesExercise = F('analysisMarker_id__analysis_id__donor_id__donortestofc_exercise__donor_ofc_exercise'),
                                                                gramLimit_OFC = F('analysisMarker_id__analysis_id__donor_id__donortestofc__gram_limit_ofc'),
                                                                OFC_class = F('analysisMarker_id__analysis_id__donor_id__donortestofc__donor_ofc'),
                                                                gramLimit_OFC_exercise = F('analysisMarker_id__analysis_id__donor_id__donortestofc_exercise__gram_limit_ofc_exercise'),
                                                                gIgE = F('analysisMarker_id__analysis_id__donor_id__donortestblood__gIgE'),
                                                                IgE_wheat_flour = F('analysisMarker_id__analysis_id__donor_id__donortestblood__wheat_flour'),
                                                                IgE_gluten = F('analysisMarker_id__analysis_id__donor_id__donortestblood__gluten'),
                                                                IgE_gliadin = F('analysisMarker_id__analysis_id__donor_id__donortestblood__gliadin'),
                                                                IgE_Tri_a_19 = F('analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_19'),
                                                                IgE_Tri_a_14 = F('analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_14'), 
                                                                IgE_Tryptase = F('analysisMarker_id__analysis_id__donor_id__donortestblood__Tryptase'), 
                                                                SPT_Histamine = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__Histamine'), 
                                                                SPT_NaCl = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__NaCl'), 
                                                                SPT_wheat_flour = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_flour'), 
                                                                SPT_wheat_gluten = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_gluten'), 
                                                                SPT_birch = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__birch'), 
                                                                SPT_mugworth = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__mugworth'), 
                                                                SPT_timothy = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__timothy'), 
                                                                SPT_house_dust_mite = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__house_dust_mite'), 
                                                                SPT_cat = F('analysisMarker_id__analysis_id__donor_id__donortest_spt__cat')).order_by('BAT_ID', 'Donor', 'Panel')
    
    bat_name = request.GET.get('bat_name')
    donor_name = request.GET.get('donor_names')
    panel_name = request.GET.get('panel_names')
    marker_name = request.GET.get('marker_names')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    allergen_name = request.GET.get('allergens')
    analysis_type = request.GET.get('analysis_type')
    file_controls = request.GET.get('file_controls')
    OFC_classes = request.GET.get('OFC_classes')
    OFC_classesExercise = request.GET.get('OFC_classesExercise')
    clinical_classes = request.GET.get('clinical_classes')
    results = request.GET.get('analysis_results')
    responders = request.GET.get('responders')
    zmarker = request.GET.get('zmarker')
    sort_by = request.GET.get('sort_by')
    redQ4_min = request.GET.get('redQ4_min')
    redQ4_max = request.GET.get('redQ4_max')
    blackQ2_min = request.GET.get('blackQ2_min')
    blackQ2_max = request.GET.get('blackQ2_max')
    blackQ3_min = request.GET.get('blackQ3_min')
    blackQ3_max = request.GET.get('blackQ3_max')
    blackQ4_min = request.GET.get('blackQ4_min')
    blackQ4_max = request.GET.get('blackQ4_max')
    zmeanQ4_min = request.GET.get('zmeanQ4_min')
    zmeanQ4_max = request.GET.get('zmeanQ4_max')
    Z1_minQ4_min = request.GET.get('Z1_minQ4_min')
    Z1_minQ4_max = request.GET.get('Z1_minQ4_max')
    Z1_maxQ4_min = request.GET.get('Z1_maxQ4_min')
    Z1_maxQ4_max = request.GET.get('Z1_maxQ4_max')
    msi_YQ4_min = request.GET.get('msi_YQ4_min')
    msi_YQ4_max = request.GET.get('msi_YQ4_max')
    cellQ4_min = request.GET.get('cellQ4_min')
    cellQ4_max = request.GET.get('cellQ4_max')
    gIgEmin = request.GET.get('gIgEmin')
    gIgEmax = request.GET.get('gIgEmax')
    wheatFlour_min = request.GET.get('wheatFlour_min')
    wheatFlour_max = request.GET.get('wheatFlour_max')
    gluten_min = request.GET.get('gluten_min')
    gluten_max = request.GET.get('gluten_max')
    gliadin_min = request.GET.get('gliadin_min')
    gliadin_max = request.GET.get('gliadin_max')
    tri_a_19_min = request.GET.get('tri_a_19_min')
    tri_a_19_max = request.GET.get('tri_a_19_max')
    tri_a_14_min = request.GET.get('tri_a_14_min')
    tri_a_14_max = request.GET.get('tri_a_14_max')
    Tryptase_min = request.GET.get('Tryptase_min')
    Tryptase_max = request.GET.get('Tryptase_max')
    Histamine_min = request.GET.get('Histamine_min')
    Histamine_max = request.GET.get('Histamine_max')
    NaCl_min = request.GET.get('NaCl_min')
    NaCl_max = request.GET.get('NaCl_max')
    wheatFlourSPT_min = request.GET.get('wheatFlourSPT_min')
    wheatFlourSPT_max = request.GET.get('wheatFlourSPT_max')
    glutenSPT_min = request.GET.get('glutenSPT_min')
    glutenSPT_max = request.GET.get('glutenSPT_max')
    birch_min = request.GET.get('birch_min')
    birch_max = request.GET.get('birch_max')
    mugworth_min = request.GET.get('mugworth_min')
    mugworth_max = request.GET.get('mugworth_max')
    timothy_min = request.GET.get('timothy_min')
    timothy_max = request.GET.get('timothy_max')
    house_dust_mite_min = request.GET.get('house_dust_mite_min')
    house_dust_mite_max = request.GET.get('house_dust_mite_max')
    cat_min = request.GET.get('cat_min')
    cat_max = request.GET.get('cat_max')
    
    compare_file_controls = request.GET.get('compare_file_controls')
    compare_allergen = request.GET.get('compare_allergen')

    AVG = request.GET.get('AVG')
    #AVG_donor = request.GET.get('AVG_donor')
    redQ4 = request.GET.get('redQ4')
    
    queryList = queryList.filter(Analysis_Version=Case(
                                                        When(Analysis_Type='AutoBat', then=Value(bat_version)),
                                                        When(Analysis_Type='AutoGrat', then=Value(grat_version))
    #bat_version
    #grat_version
                                                    )
                                )
    if bat_name != "all":
        queryList = queryList.filter(BAT_ID = bat_name)
    if is_valid_queryparam(donor_name):
        queryList = queryList.filter(Donor__icontains=donor_name)
    if panel_name !="all":
        queryList = queryList.filter(Panel = panel_name)
    elif is_valid_queryparam(marker_name):
        markers = list(models.Channels.objects.filter(pns__icontains=marker_name).values_list('analysis_id', flat=True))
        queryList = queryList.filter(analysisMarker_id__analysis_id__in=markers)
    if analysis_type != "all":
        queryList = queryList.filter(Analysis_Type=analysis_type)    
    if file_controls !="all":
        queryList = queryList.filter(Control=file_controls)
    if is_valid_queryparam(allergen_name):
        queryList = queryList.filter(Allergen__icontains=allergen_name)
    if compare_file_controls !="all" and is_valid_queryparam(compare_allergen):
        queryList = queryList.filter(Q(Allergen__icontains=compare_allergen) |  Q(Control=compare_file_controls))
    if is_valid_queryparam(date_min):
        queryList = queryList.filter(Date__gte=date_min)
    if is_valid_queryparam(date_max):
        queryList = queryList.filter(Date__lt=date_max)
    if results !="all":
        queryList = queryList.filter(result=results)
    if responders !="all":
        queryList = queryList.filter(responder=responders)
    if is_valid_queryparam(zmarker):
        queryList = queryList.filter(zMarker__icontains=zmarker)
    if clinical_classes !="all":
        if clinical_classes == 'All Classified':
            queryList = queryList.exclude(Clinical_class__isnull=True).exclude(Clinical_class__exact='')
        else:
            queryList = queryList.filter(Clinical_class=clinical_classes)
    if OFC_classes !="all":
        queryList = queryList.filter(OFC_class=OFC_classes)
    if OFC_classesExercise !="all":
        queryList = queryList.filter(OFC_classesExercise=OFC_classesExercise)
    if is_valid_queryparam(redQ4_min):
        queryList = queryList.filter(redQ4__gte=redQ4_min)
    if is_valid_queryparam(redQ4_max):
        queryList = queryList.filter(redQ4__lt=redQ4_max)
    if is_valid_queryparam(blackQ2_min):
        queryList = queryList.filter(blackQ2__gte=blackQ2_min)
    if is_valid_queryparam(blackQ2_max):
        queryList = queryList.filter(blackQ2__lt=blackQ2_max)
    if is_valid_queryparam(blackQ3_min):
        queryList = queryList.filter(blackQ3__gte=blackQ3_min)
    if is_valid_queryparam(blackQ3_max):
        queryList = queryList.filter(blackQ3__lt=blackQ3_max)
    if is_valid_queryparam(blackQ4_min):
        queryList = queryList.filter(blackQ4__gte=blackQ4_min)
    if is_valid_queryparam(blackQ4_max):
        queryList = queryList.filter(blackQ4__lt=blackQ4_max)
    if is_valid_queryparam(zmeanQ4_min):
        queryList = queryList.filter(zmeanQ4__gte=zmeanQ4_min)
    if is_valid_queryparam(zmeanQ4_max):
        queryList = queryList.filter(zmeanQ4__lt=zmeanQ4_max)
    if is_valid_queryparam(Z1_minQ4_min):
        queryList = queryList.filter(Z1_minQ4__gte=Z1_minQ4_min)
    if is_valid_queryparam(Z1_minQ4_max):
        queryList = queryList.filter(Z1_minQ4__lt=Z1_minQ4_max)
    if is_valid_queryparam(Z1_maxQ4_min):
        queryList = queryList.filter(Z1_maxQ4__gte=Z1_maxQ4_min)
    if is_valid_queryparam(Z1_maxQ4_max):
        queryList = queryList.filter(Z1_maxQ4__lt=Z1_maxQ4_max)
    if is_valid_queryparam(msi_YQ4_min):
        queryList = queryList.filter(msi_YQ4__gte=msi_YQ4_min)
    if is_valid_queryparam(msi_YQ4_max):
        queryList = queryList.filter(msi_YQ4__lt=msi_YQ4_max)
    if is_valid_queryparam(cellQ4_min):
        queryList = queryList.filter(cellQ4__gte=cellQ4_min)
    if is_valid_queryparam(cellQ4_max):
        queryList = queryList.filter(cellQ4__lt=cellQ4_max)

    if is_valid_queryparam(gIgEmin):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gIgE__gte=gIgEmin)
    if is_valid_queryparam(gIgEmax):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gIgE__lt=gIgEmax)

    if is_valid_queryparam(wheatFlour_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__wheat_flour__gte=wheatFlour_min)
    if is_valid_queryparam(wheatFlour_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__wheat_flour__lt=wheatFlour_max)
    if is_valid_queryparam(gluten_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gluten__gte=gluten_min)
    if is_valid_queryparam(gluten_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gluten__lt=gluten_max)
    if is_valid_queryparam(gliadin_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gliadin__gte=gliadin_min)
    if is_valid_queryparam(gliadin_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__gliadin__lt=gliadin_max)
    if is_valid_queryparam(tri_a_19_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_19__gte=tri_a_19_min)
    if is_valid_queryparam(tri_a_19_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_19__lt=tri_a_19_max)
    if is_valid_queryparam(tri_a_14_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_14__gte=tri_a_14_min)
    if is_valid_queryparam(tri_a_14_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tri_a_14__lt=tri_a_14_max)
    if is_valid_queryparam(Tryptase_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tryptase__gte=Tryptase_min)
    if is_valid_queryparam(Tryptase_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortestblood__Tryptase__lt=Tryptase_max)

    if is_valid_queryparam(Histamine_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__Histamine__lt=Histamine_max)
    if is_valid_queryparam(Histamine_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__Histamine__gte=Histamine_min)
    if is_valid_queryparam(NaCl_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__NaCl__gte=NaCl_min)
    if is_valid_queryparam(NaCl_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__NaCl__lt=NaCl_max)

    if is_valid_queryparam(wheatFlourSPT_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_flour__gte=wheatFlourSPT_min)
    if is_valid_queryparam(wheatFlourSPT_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_flour__lt=wheatFlourSPT_max)
    if is_valid_queryparam(glutenSPT_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_gluten__gte=glutenSPT_min)
    if is_valid_queryparam(glutenSPT_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__wheat_gluten__lt=glutenSPT_max)

    if is_valid_queryparam(birch_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__birch__gte=birch_min)
    if is_valid_queryparam(birch_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__birch__lt=birch_max)
    if is_valid_queryparam(mugworth_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__mugworth__gte=mugworth_min)
    if is_valid_queryparam(mugworth_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__mugworth__lt=mugworth_max)
    if is_valid_queryparam(timothy_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__timothy__gte=timothy_min)
    if is_valid_queryparam(timothy_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__timothy__lt=timothy_max)
    if is_valid_queryparam(house_dust_mite_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__house_dust_mite__gte=house_dust_mite_min)
    if is_valid_queryparam(house_dust_mite_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__house_dust_mite__lt=house_dust_mite_max)
    if is_valid_queryparam(cat_min):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__cat__gte=cat_min)
    if is_valid_queryparam(cat_max):
        queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donortest_spt__cat__gte=cat_max)

    """
    # sort it if applied on based on bat_name/donor_name
    if sort_by == "bat_name":
        queryList = queryList.order_by("analysisMarker_id__analysis_id__bat_id__bat_name")
    elif sort_by == "donor_name":
        queryList = queryList.order_by("analysisMarker_id__analysis_id__donor_id__donor_abbr")
    elif sort_by == "files":
        queryList = queryList.order_by("file_id__file_name")
    """
    time_stamp = time.time()
    excel_name = "None"
    if len(queryList) > 0:
        excel_name = str(request.user.last_name) + str(time_stamp) + ".xlsx"
        path = os.path.join(settings.MEDIA_ROOT, "user-data")
        create_path(path)
        excel_path = os.path.join(path, excel_name)
        writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
        df = pd.DataFrame.from_records(queryList.values('BAT_ID', 'Donor', 'Panel', 'Condition', 'Date', 'Analysis_Type', 'Analysis_Version', 'File_Name', 'Allergen', 'Control', 
                                                    'Clinical_class', 'OFC_classesExercise', 'gramLimit_OFC', 'OFC_class', 'gramLimit_OFC_exercise',
                                                    'gIgE', 'IgE_wheat_flour', 'IgE_gluten', 'IgE_gliadin', 'IgE_Tri_a_19',
                                                    'IgE_Tri_a_14', 'IgE_Tryptase', 'SPT_Histamine', 'SPT_NaCl', 'SPT_wheat_flour', 'SPT_wheat_gluten', 'SPT_birch',
                                                    'SPT_mugworth', 'SPT_timothy', 'SPT_house_dust_mite', 'SPT_cat', 'result','zMarker', 'redQ4','blackQ2',
                                                    'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4', 'msi_YQ4', 'cellQ3', 'cellQ4', 
                                                    'X_Threshold', 'Y_Threshold', 'Z2_1_Threshold', 'Z2_2_Threshold', 'responder', 'cellTotal',
                                                    'File_id', 'analysisMarker_id', 'Analysis_id'
                                                    ))
        row = 0
        first_row = True
        files_ids_list = []     
        for donor, donor_data in df.groupby(['BAT_ID','Donor','Panel','Analysis_Type', 'Analysis_Version']):  
            condition = donor_data['Control'] == 'Negative control'
            selected_row = donor_data[condition]
            new_df = pd.concat([selected_row, donor_data[~condition]])
            new_df = new_df.reset_index(drop=True)
            files_ids = []
            
            for index, r in new_df.iterrows():
                file_id = r['File_id']
                analysisMarker_id = r['analysisMarker_id']
                if r['Control'] != 'Unstained':
                    if r['Analysis_Type'] == 'AutoGrat':
                        zmarker_name = get_object_or_404(models.Channels.objects.filter(analysis_id=r['Analysis_id'], pns=r['zMarker']).values_list('pnn', flat=True))
                        plot_id = get_object_or_404(models.FilesPlots.objects.filter(file_id=file_id, 
                                                                                    analysisMarker_id=analysisMarker_id, plot_path__icontains=zmarker_name).values_list('plot_id', flat=True))
                    else:
                        plot_id = get_object_or_404(models.FilesPlots.objects.filter(file_id=file_id, analysisMarker_id=analysisMarker_id).values_list('plot_id', flat=True))
                    files_ids.append(plot_id)
            
            files_ids_list.append(files_ids)
            
            if first_row:
                new_df.to_excel(writer, sheet_name='Sheet1', columns=['BAT_ID', 'Donor', 'Panel', 'Condition', 'Date', 'Analysis_Type', 'Analysis_Version', 'File_Name', 'Allergen', 'Control',
                                                    'Clinical_class', 'OFC_classesExercise', 'gramLimit_OFC', 'OFC_class', 'gramLimit_OFC_exercise',
                                                    'gIgE', 'IgE_wheat_flour', 'IgE_gluten', 'IgE_gliadin', 'IgE_Tri_a_19',
                                                    'IgE_Tri_a_14', 'IgE_Tryptase', 'SPT_Histamine', 'SPT_NaCl', 'SPT_wheat_flour', 'SPT_wheat_gluten', 'SPT_birch',
                                                    'SPT_mugworth', 'SPT_timothy', 'SPT_house_dust_mite', 'SPT_cat', 'result','zMarker', 'redQ4','blackQ2',
                                                    'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4', 'msi_YQ4', 'cellQ3', 'cellQ4',
                                                    'X_Threshold', 'Y_Threshold', 'Z2_1_Threshold', 'Z2_2_Threshold',
                                                    'responder', 'cellTotal'], startrow=row , startcol=0)
                row = row + 1
            elif not first_row:
                new_df.to_excel(writer,sheet_name='Sheet1',columns=['BAT_ID', 'Donor', 'Panel', 'Condition', 'Date', 'Analysis_Type', 'Analysis_Version', 'File_Name', 'Allergen', 'Control',
                                                    'Clinical_class', 'OFC_classesExercise', 'gramLimit_OFC', 'OFC_class', 'gramLimit_OFC_exercise',
                                                    'gIgE', 'IgE_wheat_flour', 'IgE_gluten', 'IgE_gliadin', 'IgE_Tri_a_19',
                                                    'IgE_Tri_a_14', 'IgE_Tryptase', 'SPT_Histamine', 'SPT_NaCl', 'SPT_wheat_flour', 'SPT_wheat_gluten', 'SPT_birch',
                                                    'SPT_mugworth', 'SPT_timothy', 'SPT_house_dust_mite', 'SPT_cat', 'result','zMarker', 'redQ4','blackQ2',
                                                    'blackQ3', 'blackQ4', 'zmeanQ4', 'Z1_minQ4', 'Z1_maxQ4', 'msi_YQ4', 'cellQ3', 'cellQ4', 
                                                    'X_Threshold', 'Y_Threshold', 'Z2_1_Threshold', 'Z2_2_Threshold',
                                                    'responder', 'cellTotal'], startrow=row , startcol=0, header=False)


            row = row + len(new_df.index) + 2
            first_row = False
        writer.save()
        
    rows_count = len(queryList)
    
    if rows_count < 500:
        files_ids_name = str(request.user.last_name) + str(time_stamp) + ".csv"
        with open(os.path.join(settings.MEDIA_ROOT, "user-data", files_ids_name), "w") as f:
            wr = csv.writer(f)
            wr.writerows(files_ids_list)
    else:
        files_ids_name = None
    
    return render(request,"analysis/research_results.html",{'analysis_results':queryList, 'excel_name':str(excel_name), 'files_ids':files_ids_name, 'rows_count':rows_count})

def getBat_names(request):
    # get Results from the database 
    if request.method == "GET" and request.is_ajax():
        bat_name = models.Experiment.objects.all().values_list('bat_name').order_by('bat_name')
        bat_name = [c[0] for c in list(bat_name)]
        return JsonResponse({
            "bat_name": bat_name, 
        }, status = 200)

def getPanel_names(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        panel_name = models.Panels.objects.all().values_list('panel_name').order_by('panel_id')
        panel_name = [c[0] for c in list(panel_name)]
        return JsonResponse({"panel_name": panel_name,}, status = 200)

def getMarker_names(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        panel_name = models.Panels.objects.all().values_list('panel_name').order_by('panel_id')
        panel_name = [c[0] for c in list(panel_name)]
        return JsonResponse({"panel_name": panel_name,}, status = 200)

def getFile_controls(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        file_control = models.ExperimentFiles.objects.all().values_list('control').distinct()
        file_control = [c[0] for c in list(file_control)]
        return JsonResponse({"file_control": file_control,}, status = 200)

def getClinical_classes(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        clinicalClass_name = models.ClinicalClass_Names.objects.all().values_list('clinicalClass_name').order_by('clinicalClass_name')
        clinicalClass_name = [c[0] for c in list(clinicalClass_name)]
        clinicalClass_name.insert(0, 'All Classified')
        return JsonResponse({"clinicalClass_name": clinicalClass_name,}, status = 200)

def getResponders(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        responder = models.AnalysisResults.objects.all().values_list('responder').distinct()
        responder = [c[0] for c in list(responder)]
        return JsonResponse({"responder": responder,}, status = 200)

@login_required
def downloadResults_pdf(request, files_ids):
    with open(os.path.join(settings.MEDIA_ROOT, "user-data", files_ids), newline='') as f:
        reader = csv.reader(f)
        files_lists = list(reader)
    #files_ids = files_ids.replace('[', '')
    #files_ids = files_ids.replace(']', '')
    #files_ids = files_ids.split(',')
    #files_ids = [ int(x) for x in files_ids ]
    time_stamp = time.time()
    file_path = str(request.user.last_name) + str(time_stamp) + ".pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "user-data", file_path)
    final_list = []
    for l in files_lists:
        paths = models.FilesPlots.objects.values_list('plot_path','file_id').filter(plot_id__in=l)
        img_list = []
        for i in paths:
            img_list.append(str(i[0]))
        final_list.append(img_list)
    #file_path = '/home/abusr/autoBatWeb/auto-BAT-Web/media/user-data/cd69.pdf'
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        if len(file_name) > 0:
            file_path = str(file_name) + ".pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, "user-data", file_path)
        #image_grid(img_list, file_path, 'autobat')
        #new_pdf_list = []
        #new_pdf_list.append(img_list) #the function pdf_grid is expecting a list of lists
        pdf_grid(final_list, file_path, 'autobat')
        if os.path.exists(str(file_path)):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


@login_required
def downloadResults_xlsx(request, excel_name):
    if request.method == "POST":
        path = os.path.join(settings.MEDIA_ROOT, "user-data", excel_name)
        file_name = request.POST.get('file_name') 
        if len(file_name) > 0:
            file_name = str(file_name) + '.xlsx'
            old_path = path
            new_path = os.path.join(settings.MEDIA_ROOT, "user-data", file_name)
            #os.rename
            shutil.copyfile(old_path, new_path)
        #os.popen(f'cp {old_path}, {new_path}')
            path = new_path
        if os.path.exists(str(path)):
            with open(path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
                return response
        raise Http404
        #return render(request, 'analysis/choose_analysis_type.html')
@login_required
def files_data_CSV(request):
    
    """
    data = models.AnalysisResults.objects.values('file_id__file', 'file_id__allergen','file_id__control','analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                    'analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                    'analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc', 'result')
    """
    #data = models.Channels.objects.values('pnn','pns').distinct('pnn')
    #data = models.Channels.objects.values('pnn', 'pns', 'analysis_id', 'analysis_id__analysismarkers__analysis_type')
    #data = models.ExperimentFiles.objects.values('allergen').distinct('allergen')
    
    #return render_to_csv_response(data)
