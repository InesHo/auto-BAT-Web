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
from django.db.models import Q
from datetime import date
import config
sys.path.insert(0, os.path.join(config.AUTOBAT_PATH, 'autoBat'))
from django.conf import settings
from Data import Data
from .functions import create_path
from .tasks import run_analysis_autobat_task, run_analysis_autograt_task, proccess_files
from djqscsv import render_to_csv_response
from .serializers import ResultsSerializers
from .pagination import StandardResultsSetPagination
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum
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
    donors_data = models.Donor.objects.values('donor_id', 'donor_abbr',
                                                'donorclass_sige__wheat_flour',
                                                'donorclass_sige__gluten',
                                                'donorclass_sige__gliadin',
                                                'donorclass_sige__Tri_a_19',
                                                'donorclass_sige__Tri_a_14',
                                                'donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                'donorclass_ofc__donor_ofc')
    if request.method == 'POST':
        form = forms.DonorForm(request.POST or None)
        if form.is_valid():
            donor_abbr = form.cleaned_data['donor_abbr']
            wheat_flour = form.cleaned_data['wheat_flour']
            gluten = form.cleaned_data['gluten']
            gliadin = form.cleaned_data['gliadin']
            Tri_a_19 = form.cleaned_data['Tri_a_19']
            Tri_a_14 = form.cleaned_data['Tri_a_14']
            donor_ofc = form.cleaned_data['donor_ofc']
            donor_clinicalClass_id = form.cleaned_data['donor_clinicalClass_id']
            #new_donor = form.save(commit=False)
            #new_donor.save()
            donor_instance = models.Donor(donor_abbr=donor_abbr)
            donor_instance.user_id = request.user.id
            donor_instance.save()
            donor_id = donor_instance.donor_id
            donorClassSIGE_instance = models.DonorClass_sIgE(wheat_flour = wheat_flour,
                                                            gluten = gluten,
                                                            gliadin = gliadin,
                                                            Tri_a_19 = Tri_a_19,
                                                            Tri_a_14 = Tri_a_14 )
            donorClassSIGE_instance.user_id = request.user.id
            donorClassSIGE_instance.donor_id_id = donor_id
            donorClassSIGE_instance.save()

            DonorClass_OFC_instance = models.DonorClass_OFC(donor_ofc = donor_ofc)
            DonorClass_OFC_instance.user_id = request.user.id
            DonorClass_OFC_instance.donor_id_id = donor_id
            DonorClass_OFC_instance.save()

            DonorClass_clinical_instance = models.DonorClass_clinical(donor_clinicalClass_id = donor_clinicalClass_id)
            DonorClass_clinical_instance.user_id = request.user.id
            DonorClass_clinical_instance.donor_id_id = donor_id
            DonorClass_clinical_instance.save()
            return render(request,"donors/show_donors.html",{'donors_data':donors_data})
    else:
        form = forms.DonorForm()

    context = {
        "form": form
    }
    return render(request, 'donors/add_donors.html', context=context)

@login_required
def show_donor(request):  
    donors_data = models.Donor.objects.values('donor_id', 'donor_abbr',
                                                'donorclass_sige__wheat_flour',
                                                'donorclass_sige__gluten',
                                                'donorclass_sige__gliadin',
                                                'donorclass_sige__Tri_a_19',
                                                'donorclass_sige__Tri_a_14',
                                                'donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                'donorclass_ofc__donor_ofc')

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
                analysis_instance = models.Analysis(bat_id=bat_id, donor_id=donor_id, panel_id=panel_id)
                analysis_instance.user_id = request.user.id
                analysis_instance.save()
                analysis_id = analysis_instance.analysis_id
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

        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        chosen_z1 = request.POST.get('z1')
        chosen_z1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z1).values_list('pns', flat=True))
        chosen_y1 = request.POST.get('y1')
        chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))
        chosen_z2 = request.POST.get('z2')
        analysis_date = str(date.today())
        analysis_status = "Waiting"
        analysis_type = "AutoBat"
        analysis_type_version = "1.0"
        user_id = request.user.id

        # Checking if the Experment has alrady been Analyzed with those markers
        analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                chosen_z1 = chosen_z1,
                                                chosen_y1=chosen_y1,
                                                chosen_z2=chosen_z2,
                                                analysis_type=analysis_type,
                                                analysis_id = analysis_id) 
        if not analysismarkers_data:

            analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_z1,
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
            
            outputPDFname = f"Autobat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.png"
            pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/") 
            pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/")       
            create_path(pathToExports)
            pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autobat/")
            create_path(pathToOutput)
            pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
            rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
            run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_z1_lable, chosen_y1,
                                chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports, 
                                pathToOutput, pathToGatingFunctions, rPath, user_id
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

        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        chosen_x = request.POST.get('X')
        chosen_x_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_x).values_list('pns', flat=True))
        chosen_y1 = request.POST.get('Y')
        chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))
        chosen_z2 = request.POST.get('Z2')
        chosen_z2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2).values_list('pns', flat=True))
        analysis_date = str(date.today())
        analysis_status = "Waiting"
        analysis_type = "AutoGrat"
        analysis_type_version = "1.0"
        user_id = request.user.id

        # Checking if the Experment has alrady been Analyzed with those markers
        analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                chosen_z1 = chosen_x,
                                                chosen_y1=chosen_y1,
                                                chosen_z2=chosen_z2,
                                                analysis_type=analysis_type,
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
            
            outputPDFname = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_x}_{chosen_y1}_{chosen_z2}.png"
            pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/") 
            pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/")       
            create_path(pathToExports)
            pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autograt/")
            create_path(pathToOutput)
            pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
            rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
            run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_x, chosen_x_lable, chosen_y1, chosen_y1_lable, chosen_z2, chosen_z2_lable,
                                device, outputPDFname, pathToData, pathToExports, 
                                pathToOutput, pathToGatingFunctions, rPath, user_id
                                )
            return render(request, 'analysis/analysis_ready.html')
        else:
            return render(request, 'analysis/analysis_error.html', {'analysis_id':analysis_id})
        
@login_required
def results_to_CSV(request):
    analysisResults = models.AnalysisResults.objects.values('analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'file_id__file_name', "analysisMarker_id__analysis_error", "analysisMarker_id__analysis_info_messages",
                                                            'redQ4', 'result', 'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'CD63min', 'CD63max', 'msiCCR3', 'cellQ4', 'responder')
    return render_to_csv_response(analysisResults)

@login_required
def thresholds_to_CSV(request):
    thresholds = models.AnalysisThresholds.objects.values('analysisMarker_id__analysis_id__bat_id__bat_name','analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name','SSCA_Threshold', 'FcR_Threshold', 'CD63_Threshold',
                                                            "analysisMarker_id__analysis_error", "analysisMarker_id__analysis_info_messages"
                                                            )
    return render_to_csv_response(thresholds)


@login_required
def re_analysis_all(request):
    user_id = request.user.id

    analysisMarker_obj = models.AnalysisMarkers.objects.values_list('analysisMarker_id', 'analysis_status').filter(analysis_status='Ready')

    for analysismarker in analysisMarker_obj:
        analysisMarker_id = analysismarker[0]
        analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
        """
        models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        models.FilesPlots.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        models.AnalysisResults.objects.filter(analysisMarker_id=analysisMarker_id).delete()
        """
        analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))
        bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
        donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
        panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        chosen_z1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z1', flat=True))
        chosen_y1 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_y1', flat=True))
        chosen_z2 = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('chosen_z2', flat=True))

        chosen_z1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z1).values_list('pns', flat=True))
        chosen_y1_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_y1).values_list('pns', flat=True))

        device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
        device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))

        outputPDFname = f"AutoBat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.png"
        pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/")
        pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/")
        create_path(pathToExports)
        pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autobat/")
        create_path(pathToOutput)
        pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
        rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")
 
        if analysis_type == 'AutoBat':
            """
            run_analysis_autobat_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_z1_lable, chosen_y1,
                                chosen_y1_lable, chosen_z2, device, outputPDFname, pathToData, pathToExports,
                                pathToOutput, pathToGatingFunctions, rPath, user_id
                                )
            """
            pass
        if analysis_type == 'AutoGrat':
            models.AnalysisFiles.objects.filter(analysisMarker_id=analysisMarker_id).delete()
            models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).delete()
            models.FilesPlots.objects.filter(analysisMarker_id=analysisMarker_id).delete()
            models.AnalysisResults.objects.filter(analysisMarker_id=analysisMarker_id).delete()
            models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).update(analysis_status="Waiting")

            chosen_x = chosen_z1
            chosen_x_lable = chosen_z1_lable
            chosen_z2_lable = get_object_or_404(models.Channels.objects.filter(analysis_id=analysis_id, pnn=chosen_z2).values_list('pns', flat=True))
            outputPDFname = f"AutoGrat_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.png"
            pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/autograt/")
            run_analysis_autograt_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_x, chosen_x_lable, chosen_y1, chosen_y1_lable, chosen_z2,
                                chosen_z2_lable, device, outputPDFname, pathToData, pathToExports, pathToOutput, pathToGatingFunctions, rPath, user_id
                                )
    return render(request, 'analysis/analysis_ready.html')

@login_required
def show_analysis(request):
    user_is_superuser = request.user.is_superuser
    analysis = models.Analysis.objects.values_list('analysis_id', 'bat_id','donor_id', 'panel_id').order_by('bat_id').reverse()
    analysisList = []
    for i in analysis:
        analysis_id = i[0]
        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=i[1]).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=i[2]).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=i[3]).values_list('panel_name', flat=True))       
        analysismarkers = models.AnalysisMarkers.objects.values_list('analysisMarker_id','chosen_z1', 'chosen_y1','chosen_z2', 'analysis_date',
                                                    'analysis_start_time', 'analysis_end_time','analysis_status', 'analysis_type', 'analysis_type_version'
                                                    ).filter(analysis_id = analysis_id).order_by('analysisMarker_id').reverse()
    
        if not analysismarkers:
            analysis_dict = {}
            analysis_dict['analysis_id'] = analysis_id
            analysis_dict['bat_name'] = bat_name
            analysis_dict['donor_name'] = donor_name
            analysis_dict['panel_name'] = panel_name

            analysis_dict['analysisMarker_id'] = None
            analysis_dict['chosen_z1'] = None
            analysis_dict['chosen_y1'] = None
            analysis_dict['chosen_z2'] = None
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
                analysis_dict['analysisMarker_id'] = j[0]
                analysis_dict['chosen_z1'] = j[1]
                analysis_dict['chosen_y1'] = j[2]
                analysis_dict['chosen_z2'] = j[3]
                analysis_dict['analysis_date'] = j[4]
                analysis_dict['analysis_start_time'] = j[5]
                analysis_dict['analysis_end_time'] = j[6]
                analysis_dict['analysis_status'] = j[7]
                analysis_dict['analysis_type'] = j[8]
                analysis_dict['analysis_type_version'] = j[9]
                analysisList.append(analysis_dict)
    return render(request, 'analysis/analysis_list.html',{'analysis':analysisList, 'user_is_superuser':user_is_superuser})


@login_required
def delete_analysis_alert(request, analysisMarker_id):
    return render(request, 'analysis/analysis_delete_alert.html', {'analysisMarker_id':analysisMarker_id})


@login_required
def re_analysis_alert(request):
    return render(request, 'analysis/re_analysis_alert.html')

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
    SSCA_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('SSCA_Threshold', flat=True))
    FcR_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('FcR_Threshold', flat=True))
    CD63_Threshold = get_object_or_404(models.AnalysisThresholds.objects.filter(analysisMarker_id=analysisMarker_id).values_list('CD63_Threshold', flat=True))
    analysis_id = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_id', flat=True))
    bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
    donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
    panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))
    bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
    donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
    panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))
    analysis_type = get_object_or_404(models.AnalysisMarkers.objects.filter(analysisMarker_id=analysisMarker_id).values_list('analysis_type', flat=True))

    return render(request,"analysis/list_thresholds.html",{'SSCA_Threshold':SSCA_Threshold,'FcR_Threshold':FcR_Threshold,'CD63_Threshold':CD63_Threshold,
                                                           'bat_name': bat_name,'donor_name': donor_name, 'panel_name': panel_name,
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
                                                            'analysisMarker_id__analysis_type',
                                                            'file_id__file_name', 'file_id__allergen','file_id__control',
                                                            'redQ4', 'result', 'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'z1_min', 'z1_max', 'msi_Y', 'cellQ4', 'responder')


    return render(request,"analysis/analysis_report.html",{'analysis_results':analysisResults})

@login_required
def thresholds_report(request):


    analysisThresholds = models.AnalysisThresholds.objects.values('analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'SSCA_Threshold', 'FcR_Threshold', 'CD63_Threshold', 'analysisMarker_id__chosen_z1'
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



######################################################################

def research_questions(request):
    return render(request, "analysis/research_questions.html", {})

def is_valid_queryparam(param):
    return param != '' and param is not None

class ListResults(ListAPIView):
    # set the pagination and serializer class
    pagination_class = StandardResultsSetPagination
    serializer_class = ResultsSerializers
    def get_queryset(self):
        # filter the queryset based on the filters applied
        queryList = models.AnalysisResults.objects.values(  'id',
                                                            'analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_id__bat_id__date_of_measurement',
                                                            'analysisMarker_id__analysis_type',
                                                            'file_id','file_id__file_name', 'file_id__allergen','file_id__control',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14',
                                                            'redQ4', 'result', 'blackQ2', 'blackQ3', 'blackQ4', 'zmeanQ4', 'z1_min', 'z1_max', 'msi_Y', 'cellQ4', 'responder')
        bat_name = self.request.query_params.get('bat_name', None)
        donor_name = self.request.query_params.get('donor_name', None)
        panel_name = self.request.query_params.get('panel_name', None)
        marker_name = self.request.query_params.get('marker_name', None)
        date_min = self.request.query_params.get('date_min', None)
        date_max = self.request.query_params.get('date_max', None)
        allergen_name = self.request.query_params.get('allergens', None)
        analysis_type = self.request.query_params.get('analysis_type', None)
        file_controls = self.request.query_params.get('file_controls', None)
        OFC_classes = self.request.query_params.get('OFC_classes', None)
        clinical_classes = self.request.query_params.get('clinical_classes', None)
        results = self.request.query_params.get('analysis_results', None)
        responders = self.request.query_params.get('responders', None)
        sort_by = self.request.query_params.get('sort_by', None)
        redQ4_min = self.request.query_params.get('redQ4_min', None)
        redQ4_max = self.request.query_params.get('redQ4_max', None)
        blackQ2_min = self.request.query_params.get('blackQ2_min', None)
        blackQ2_max = self.request.query_params.get('blackQ2_max', None)
        blackQ3_min = self.request.query_params.get('blackQ3_min', None)
        blackQ3_max = self.request.query_params.get('blackQ3_max', None)
        blackQ4_min = self.request.query_params.get('blackQ4_min', None)
        blackQ4_max = self.request.query_params.get('blackQ4_max', None)
        zmeanQ4_min = self.request.query_params.get('zmeanQ4_min', None)
        zmeanQ4_max = self.request.query_params.get('zmeanQ4_max', None)
        z1_min_min = self.request.query_params.get('z1_min_min', None)
        z1_min_max = self.request.query_params.get('z1_min_max', None)
        z1_max_min = self.request.query_params.get('z1_max_min', None)
        z1_max_max = self.request.query_params.get('z1_max_max', None)
        msi_Y_min = self.request.query_params.get('msi_Y_min', None)
        msi_Y_max = self.request.query_params.get('msi_Y_max', None)
        cellQ4_min = self.request.query_params.get('cellQ4_min', None)
        cellQ4_max = self.request.query_params.get('cellQ4_max', None)
        wheatFlour_min = self.request.query_params.get('wheatFlour_min', None)
        wheatFlour_max = self.request.query_params.get('wheatFlour_max', None)
        gluten_min = self.request.query_params.get('gluten_min', None)
        gluten_max = self.request.query_params.get('gluten_max', None)
        gliadin_min = self.request.query_params.get('gliadin_min', None)
        gliadin_max = self.request.query_params.get('gliadin_max', None)
        tri_a_19_min = self.request.query_params.get('tri_a_19_min', None)
        tri_a_19_max = self.request.query_params.get('tri_a_19_max', None)
        tri_a_14_min = self.request.query_params.get('tri_a_14_min', None)
        tri_a_14_max = self.request.query_params.get('tri_a_14_max', None)
        AVR_sample = self.request.query_params.get('AVR_sample', None)
        AVR_donor = self.request.query_params.get('AVR_donor', None)
        
        if AVR_sample == "Avg":
            pass
            """
            queryList = models.AnalysisResults.objects.values('analysisMarker_id__analysis_id',
                                                            'analysisMarker_id__analysis_id__bat_id__bat_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__panel_id',
                                                            'analysisMarker_id__analysis_id__panel_id__panel_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14',
                                                            ).annotate(file_id__file_name=Count('file_id__file_name'), file_id__allergen=Count('file_id__allergen', distinct=True),
                                                                    file_id__control=Count('file_id__control', distinct=True),
                                                                    analysisMarker_id__analysis_id__bat_id__date_of_measurement=Count(
                                                                        'analysisMarker_id__analysis_id__bat_id__date_of_measurement', distinct=True),
                                                                    redQ4=Avg('redQ4'),  blackQ2=Avg('blackQ2'), result=Count('result', distinct=True), blackQ3=Avg('blackQ3'), blackQ4=Avg('blackQ4'),
                                                                    zmeanQ4=Avg('zmeanQ4'), z1_min=Avg('z1_min'), CD63max=Avg('z1_max'),
                                                                    msi_Y=Avg('msi_Y'), cellQ4=Sum('cellQ4'), responder=Count('responder', distinct=True))
            """
        if AVR_donor == "Avg":
            pass
            """
            queryList = models.AnalysisResults.objects.values('analysisMarker_id__analysis_id__donor_id__donor_abbr',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19',
                                                            'analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14',
                                                            ).annotate(analysisMarker_id__analysis_id=Count('analysisMarker_id__analysis_id', distinct=True),
                                                                    file_id__file_name=Count('file_id__file_name'), file_id__allergen=Count('file_id__allergen', distinct=True),
                                                                    file_id__control=Count('file_id__control', distinct=True),
                                                                    analysisMarker_id__analysis_id__bat_id__bat_name=Count('analysisMarker_id__analysis_id__bat_id__bat_name', distinct=True),
                                                                    analysisMarker_id__analysis_id__panel_id__panel_name=Count('analysisMarker_id__analysis_id__panel_id__panel_name', distinct=True),
                                                                    analysisMarker_id__analysis_id__bat_id__date_of_measurement=Count(
                                                                        'analysisMarker_id__analysis_id__bat_id__date_of_measurement', distinct=True),
                                                                    redQ4=Avg('redQ4'),  blackQ2=Avg('blackQ2'), result=Count('result', distinct=True), blackQ3=Avg('blackQ3'), blackQ4=Avg('blackQ4'),
                                                                    zmeanQ4=Avg('zmeanQ4'), z1_min=Avg('z1_min'), CD63max=Avg('z1_max'),
                                                                    msi_Y=Avg('msi_Y'), cellQ4=Sum('cellQ4'), responder=Count('responder', distinct=True))
            """
        if bat_name:
            queryList = queryList.filter(analysisMarker_id__analysis_id__bat_id__bat_name = bat_name)
        if is_valid_queryparam(donor_name):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donor_abbr__icontains=donor_name)
        if panel_name:
            queryList = queryList.filter(analysisMarker_id__analysis_id__panel_id__panel_name = panel_name)
        if is_valid_queryparam(marker_name):
            markers = list(models.Channels.objects.filter(pns__icontains=marker_name).values_list('analysis_id', flat=True))
            queryList = queryList.filter(analysisMarker_id__analysis_id__in=markers)
        if is_valid_queryparam(allergen_name):
            queryList = queryList.filter(file_id__allergen__icontains=allergen_name)
        if is_valid_queryparam(analysis_type):
            queryList = queryList.filter(analysisMarker_id__analysis_type=analysis_type)
        if is_valid_queryparam(file_controls):
            queryList = queryList.filter(file_id__control=file_controls)
        if is_valid_queryparam(date_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__bat_id__date_of_measurement__gte=date_min)
        if is_valid_queryparam(date_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__bat_id__date_of_measurement__lt=date_max)
        if is_valid_queryparam(results):
            queryList = queryList.filter(result=results)
        if is_valid_queryparam(responders):
            queryList = queryList.filter(responder=responders)
        if is_valid_queryparam(clinical_classes):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_clinical__donor_clinicalClass_id__clinicalClass_name=clinical_classes)
        if is_valid_queryparam(OFC_classes):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_ofc__donor_ofc=OFC_classes)
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
        if is_valid_queryparam(z1_min_min):
            queryList = queryList.filter(z1_min__gte=z1_min_min)
        if is_valid_queryparam(z1_min_max):
            queryList = queryList.filter(z1_min__lt=z1_min_max)
        if is_valid_queryparam(z1_max_min):
            queryList = queryList.filter(z1_max__gte=z1_max_min)
        if is_valid_queryparam(z1_max_max):
            queryList = queryList.filter(z1_max__lt=z1_max_max)
        if is_valid_queryparam(msi_Y_min):
            queryList = queryList.filter(msi_Y__gte=msi_Y_min)
        if is_valid_queryparam(msi_Y_max):
            queryList = queryList.filter(msi_Y__lt=msi_Y_max)
        if is_valid_queryparam(cellQ4_min):
            queryList = queryList.filter(cellQ4__gte=cellQ4_min)
        if is_valid_queryparam(cellQ4_max):
            queryList = queryList.filter(cellQ4__lt=cellQ4_max)
        if is_valid_queryparam(wheatFlour_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour__gte=wheatFlour_min)
        if is_valid_queryparam(wheatFlour_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__wheat_flour__lt=wheatFlour_max)
        if is_valid_queryparam(gluten_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten__gte=gluten_min)
        if is_valid_queryparam(gluten_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__gluten__lt=gluten_max)
        if is_valid_queryparam(gliadin_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin__gte=gliadin_min)
        if is_valid_queryparam(gliadin_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__gliadin__lt=gliadin_max)
        if is_valid_queryparam(tri_a_19_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19__gte=tri_a_19_min)
        if is_valid_queryparam(tri_a_19_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_19__lt=tri_a_19_max)
        if is_valid_queryparam(tri_a_14_min):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14__gte=tri_a_14_min)
        if is_valid_queryparam(tri_a_14_max):
            queryList = queryList.filter(analysisMarker_id__analysis_id__donor_id__donorclass_sige__Tri_a_14__lt=tri_a_14_max)

        # sort it if applied on based on bat_name/donor_name
        if sort_by == "bat_name":
            queryList = queryList.order_by("analysisMarker_id__analysis_id__bat_id__bat_name")
        elif sort_by == "donor_name":
            queryList = queryList.order_by("analysisMarker_id__analysis_id__donor_id__donor_abbr")
        elif sort_by == "files":
            queryList = queryList.order_by("file_id__file_name")


        return queryList


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
        return JsonResponse({"clinicalClass_name": clinicalClass_name,}, status = 200)

def getResponders(request):
    # get Results from the database
    if request.method == "GET" and request.is_ajax():
        responder = models.AnalysisResults.objects.all().values_list('responder').distinct()
        responder = [c[0] for c in list(responder)]
        return JsonResponse({"responder": responder,}, status = 200)
