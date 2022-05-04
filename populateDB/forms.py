from django.contrib.auth.models import User
from django import forms
from .models import Institutes, Departments, Experimenters, Cytometers, Devices, Markers, Experiment, Donor, Panels, ExperimentFiles, FileType



class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class InstitutesForm(forms.ModelForm):
    class Meta: 
        model = Institutes 
        fields = "__all__"   


class DepartmentsForm(forms.ModelForm):  
    class Meta:  
        model = Departments  
        fields = "__all__"  


class ExperimentersForm(forms.ModelForm):
    class Meta: 
        model = Experimenters 
        fields = "__all__"   


class CytometersForm(forms.ModelForm):  
    class Meta:  
        model = Cytometers  
        fields = "__all__"  


class DevicesForm(forms.ModelForm):  
    class Meta:  
        model = Devices  
        fields = "__all__"  


class MarkersForm(forms.ModelForm):
    class Meta: 
        model = Markers 
        fields = "__all__"   

class DonorForm(forms.ModelForm):  
    class Meta:  
        model = Donor  
        fields = "__all__"  

class PanelsForm(forms.ModelForm):  
    class Meta:  
        model = Panels  
        fields = "__all__"  

class DateInput(forms.DateInput):
    input_type = 'date'

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = "__all__"
        widgets = {
            'date_of_measurement': DateInput(attrs={'type': 'date'}),
        }

class FileTypesForm(forms.ModelForm):  
    class Meta:  
        model = FileType  
        fields = "__all__"  

class ExperimentFilesForm(forms.ModelForm):
    class Meta:
        model = ExperimentFiles
        fields = "__all__" 