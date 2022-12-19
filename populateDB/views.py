from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.views.generic import View
from django.template.loader import render_to_string
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
from .tasks import run_analysis_task, proccess_files

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
    experiment_data = models.Experiment.objects.all() 
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
    donors_data = models.Donor.objects.all().order_by('donor_id').reverse()
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
    donors_data = models.Donor.objects.all().order_by('donor_id').reverse()
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
                    file_instance = models.ExperimentFiles(file_name = f, file=file_path, allergen=allergen, control=control, analysis_id=analysis_id)
                    file_instance.save()
                    
                    us_file_path = file_path


                data1 = Data(filetype="FCS", filename = us_file_path)
                data = data1.getData()
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
                                            analysis_id = analysis_id,
                                            )
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
    return render(request,"channels/show_channels.html",{'channels_data':channels_data})

def marker_settings(request, analysis_id): 
    analysis_id = analysis_id
    channels = models.Channels.objects.filter(pnn__endswith=("A") ,analysis_id = analysis_id).order_by('channel_id')
    return render(request, 'analysis/marker_settings.html', {'channels': channels, 'analysis_id': analysis_id}) 
  
@login_required
def run_analysis(request, analysis_id):

    if request.method == "POST":

        bat_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('bat_id', flat=True))
        donor_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('donor_id', flat=True))
        panel_id = get_object_or_404(models.Analysis.objects.filter(analysis_id=analysis_id).values_list('panel_id', flat=True))

        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=donor_id).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=panel_id).values_list('panel_name', flat=True))

        chosen_z1 = request.POST.get('z1')
        chosen_y1 = request.POST.get('y1')
        chosen_z2 = request.POST.get('z2')
        analysis_date = str(date.today())
        analysis_status = "Waitting"
        analysis_type = "Auto Bat"

        # Checking if the Experment has alrady been Analyzed with those markers
        analysismarkers_data = models.AnalysisMarkers.objects.values_list('chosen_z1','chosen_y1','chosen_z2').filter(
                                                chosen_z1 = chosen_z1,
                                                chosen_y1=chosen_y1,
                                                chosen_z2=chosen_z2,
                                                analysis_id = analysis_id) 

        if not analysismarkers_data:

            analysismarkers_instance = models.AnalysisMarkers(chosen_z1=chosen_z1,
                                                        chosen_y1=chosen_y1,
                                                        chosen_z2=chosen_z2,
                                                        analysis_date=analysis_date,
                                                        analysis_status=analysis_status,
                                                        analysis_type=analysis_type,
                                                        analysis_id=analysis_id
                                                        )
            analysismarkers_instance.save()
            
            analysisMarker_id = analysismarkers_instance.analysisMarker_id


            device_id = get_object_or_404(models.Experiment.objects.filter(bat_id=bat_id).values_list('device_id', flat=True))
            device = get_object_or_404(models.Devices.objects.filter(device_id=device_id).values_list('device_label', flat=True))

            outputPDFname = f"Autogated_{bat_name}_{donor_name}_{panel_name}_{chosen_z1}_{chosen_y1}_{chosen_z2}.png "
            pathToData = os.path.join(settings.MEDIA_ROOT, f"FCS_fiels/{bat_name}/{donor_name}/{panel_name}/") 
            pathToExports = os.path.join(settings.MEDIA_ROOT, f"gated_files/{bat_name}/{donor_name}/{panel_name}/")       
            create_path(pathToExports)
            pathToOutput = os.path.join(settings.MEDIA_ROOT, f"output/{bat_name}/{donor_name}/{panel_name}/")
            create_path(pathToOutput)
            pathToGatingFunctions = os.path.join(config.AUTOBAT_PATH, "functions/preGatingFunc.R")
            rPath = os.path.join(config.AUTOBAT_PATH, "functions/YH_binplot_functions.R")

            run_analysis_task(analysis_id, analysisMarker_id, bat_name, donor_name, panel_name, chosen_z1, chosen_y1,
                                chosen_z2, device, outputPDFname, pathToData, pathToExports, 
                                pathToOutput, pathToGatingFunctions, rPath
                                )
            return render(request, 'analysis/analysis_ready.html')
        else:
            return render(request, 'analysis/analysis_error.html', {'analysis_id':analysis_id})

@login_required
def show_analysis(request):
    analysis = models.Analysis.objects.values_list('analysis_id', 'bat_id','donor_id', 'panel_id').order_by('analysis_id').reverse()
    analysisList = []
    for i in analysis:
        analysis_id = i[0]
        bat_name = get_object_or_404(models.Experiment.objects.filter(bat_id=i[1]).values_list('bat_name', flat=True))
        donor_name = get_object_or_404(models.Donor.objects.filter(donor_id=i[2]).values_list('donor_abbr', flat=True))
        panel_name = get_object_or_404(models.Panels.objects.filter(panel_id=i[3]).values_list('panel_name', flat=True))       
        analysismarkers = models.AnalysisMarkers.objects.values_list('analysisMarker_id','chosen_z1', 'chosen_y1','chosen_z2', 'analysis_date',
                                                    'analysis_start_time', 'analysis_end_time','analysis_status', 'analysis_type', 'analysisMarker_id'
                                                    ).filter(analysis_id = analysis_id).order_by('analysisMarker_id').reverse()
        for j in analysismarkers:
            analysis_dict = {}
            analysis_dict['analysisMarker_id'] = j[9]
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
            analysisList.append(analysis_dict)
    return render(request, 'analysis/analysis_list.html',{'analysis':analysisList})

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
