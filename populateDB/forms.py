from django.contrib.auth.models import User
from django import forms
from . import models

class AddUserForm(forms.ModelForm):
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

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class InstitutesForm(forms.ModelForm):
    class Meta: 
        model = models.Institutes 
        fields = "__all__"   

class DepartmentsForm(forms.ModelForm):  
    class Meta:  
        model = models.Departments  
        fields = "__all__"  

class ExperimentersForm(forms.ModelForm):
    class Meta: 
        model = models.Experimenters 
        fields = "__all__"   

class DevicesForm(forms.ModelForm):  
    class Meta:  
        model = models.Devices  
        fields = "__all__"  

class DonorForm(forms.ModelForm):  
    class Meta:  
        model = models.Donor  
        fields = "__all__"  

class PanelsForm(forms.ModelForm):  
    class Meta:  
        model = models.Panels
        fields = "__all__"  

class DateInput(forms.DateInput):
    input_type = 'date'

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = models.Experiment
        fields = "__all__"
        widgets = {
            'date_of_measurement': DateInput(attrs={'type': 'date'}),
        }

class ExperimentFilesForm(forms.ModelForm):
    bat_id = forms.ModelChoiceField(queryset=models.Experiment.objects.all().order_by('bat_id'))
    donor_id = forms.ModelChoiceField(queryset=models.Donor.objects.all().order_by('donor_abbr'))
    panel_id = forms.ModelChoiceField(queryset=models.Panels.objects.all())
    class Meta:
        model = models.ExperimentFiles
        fields = ('file',)
        
        widgets = {
            'file_id' : forms.Select(attrs={'class':'form-control'}),
            'bat_id' : forms.Select(attrs={'class':'Textarea'} ),
            'donor_id' : forms.Select(attrs={'class':'form-control'}),
            'panel_id' : forms.Select(attrs={'class':'form-control'}),
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
            }

class UpdateFilesForm(forms.ModelForm):
    file_id = forms.IntegerField(min_value=1, required=True)
    class Meta:
        model = models.ExperimentFiles
        fields = ('file_id', 'file_name', 'allergen', 'control')
        widgets = {
            'file_id' : forms.TextInput(attrs={'size':'2'}),
            'file_name' : forms.TextInput(attrs={'size':'30'}),
            'allergen' : forms.TextInput(attrs={'size':'10'})

            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file_id'].widget = forms.HiddenInput()

class ChannelsForm(forms.ModelForm):
    channel_id = forms.IntegerField(min_value=1, required=True)

    class Meta:  
        model = models.Channels
        fields = ("channel_id", "pnn", "pns")
        widgets = {
            'channel_id' : forms.TextInput(attrs={'size':'3'}),
            'pnn' : forms.TextInput(attrs={'size':'15'}),
            'pns' : forms.TextInput(attrs={'size':'15'}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['channel_id'].disabled = True
        self.fields['pnn'].disabled = True
        self.fields['channel_id'].widget = forms.HiddenInput()

class MarkerSettingsForm(forms.Form):
    z1 = forms.ModelChoiceField(queryset=models.Channels.objects.all())
    y1 = forms.ModelChoiceField(queryset=models.Channels.objects.all())
    z2 = forms.ModelChoiceField(queryset=models.Channels.objects.all())
    class Meta:
        fields = ("z1", "y1", "z2")
        widgets = {
            'z1' : forms.Select(attrs={'class':'form-control'}),
            'y1' : forms.Select(attrs={'class':'form-control'}),
            'z2' : forms.Select(attrs={'class':'form-control'}),
            }

class MetaDataForm(forms.ModelForm):  
    class Meta:  
        model = models.MetaData  
        fields = "__all__" 


class MeanRawDataForm(forms.ModelForm):  
    class Meta:  
        model = models.MeanRawData  
        fields = "__all__"

class AnalysisForm(forms.ModelForm):
	analysis_date = forms.DateTimeInput()
	class Meta:
		model = models.Analysis
		fields = ('bat_id', 'donor_id', 'panel_id')
