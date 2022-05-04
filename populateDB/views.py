from django.http import request
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ExperimentFilesForm, UserRegistration, UserEditForm, InstitutesForm, DepartmentsForm, ExperimentersForm, CytometersForm, DevicesForm, MarkersForm, DonorForm, PanelsForm, ExperimentForm, FileTypesForm
from .models import ExperimentFiles, Experiment, Donor, Institutes
from django.views.generic import View
from django.http import JsonResponse


# Create your views here.

@login_required
def home(request):
    num_bats = Experiment.objects.all().count()
    num_donors = Donor.objects.all().count()
    num_files = ExperimentFiles.objects.all().count()
    context = {
        "welcome": "Welcome to The Auto-Bat Web",
        'num_bats': num_bats,
        'num_donors': num_donors,
        'num_files': num_files
    }
    return render(request, 'home.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'auth/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'auth/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'add.html', context=context)

@login_required
def experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST or None)
        if form.is_valid():
            new_experiment = form.save(commit=False)
            new_experiment.save()
            experiment_data = Experiment.objects.all() 
            return render(request,"expermiments/show_experiment.html",{'experiment_data':experiment_data})
            #return render(request, 'expermiments/show_experiment.html')
    else:
        form = ExperimentForm()

    
    context = {
        "form": form
    }
    
    return render(request, 'expermiments/add_experiment.html', context=context)

@login_required
def show_experiment(request):  
    experiment_data = Experiment.objects.all() 
    return render(request,"expermiments/show_experiment.html",{'experiment_data':experiment_data})  

@login_required
def institute(request):
    if request.method == 'POST':
        form = InstitutesForm(request.POST or None)
        if form.is_valid():
            new_institute = form.save(commit=False)
            new_institute.save()
            
            return render(request, 'home.html')
    else:
        form = InstitutesForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)



@login_required
def department(request):
    if request.method == 'POST':
        form = DepartmentsForm(request.POST or None)
        if form.is_valid():
            new_experiment = form.save(commit=False)
            new_experiment.save()
            return render(request, 'home.html')
    else:
        form = DepartmentsForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def experimenter(request):
    if request.method == 'POST':
        form = ExperimentersForm(request.POST or None)
        if form.is_valid():
            new_experimenter = form.save(commit=False)
            new_experimenter.save()
            return render(request, 'home.html')
    else:
        form = ExperimentersForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def cytometer(request):
    if request.method == 'POST':
        form = CytometersForm(request.POST or None)
        if form.is_valid():
            new_cytometer = form.save(commit=False)
            new_cytometer.save()
            return render(request, 'home.html')
    else:
        form = CytometersForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def device(request):
    if request.method == 'POST':
        form = DevicesForm(request.POST or None)
        if form.is_valid():
            new_device = form.save(commit=False)
            new_device.save()
            return render(request, 'home.html')
    else:
        form = DevicesForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def marker(request):
    if request.method == 'POST':
        form = MarkersForm(request.POST or None)
        if form.is_valid():
            new_marker = form.save(commit=False)
            new_marker.save()
            return render(request, 'home.html')
    else:
        form = MarkersForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST or None)
        if form.is_valid():
            new_donor = form.save(commit=False)
            new_donor.save()
            return render(request, 'home.html')
    else:
        form = DonorForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def panel(request):
    if request.method == 'POST':
        form = PanelsForm(request.POST or None)
        if form.is_valid():
            new_panel = form.save(commit=False)
            new_panel.save()
            return render(request, 'home.html')
    else:
        form = PanelsForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)

@login_required
def filetype(request):
    if request.method == 'POST':
        form = FileTypesForm(request.POST or None)
        if form.is_valid():
            new_filetype = form.save(commit=False)
            new_filetype.save()
            return render(request, 'home.html')
    else:
        form = FileTypesForm()

    context = {
        "form": form
    }

    return render(request, 'add.html', context=context)


def show_experimentfile(request):  
    file_data = ExperimentFiles.objects.all() 
    return render(request,"files/show_files.html",{'file_data':file_data}) 


class experimentfile(View):

    def get(self, request):
        form = ExperimentFilesForm()

        return render(request, 'files/add_files.html', context={'form':form})

    def post(self, request):
        if request.method=='POST':
            form = ExperimentFilesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'data':'Data uploaded'})

            else:
                return JsonResponse({'data':'Something went wrong!!'})

            


