from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
import os
import sys


class Institutes(models.Model):

    institute_id = models.AutoField(primary_key=True)      
    institute_shortName = models.CharField(max_length=15, blank = False, unique = True)     
    institute_name = models.CharField(max_length=150, blank = True)    
    institute_address = models.CharField(max_length=150,  blank = True)  
    institute_email = models.EmailField(blank = True)
    institute_phoneNumber = models.CharField(max_length=20, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return (self.institute_shortName) 

class Departments(models.Model):

    department_id = models.AutoField(primary_key=True)      
    department_name = models.CharField(max_length=150, unique=True, blank = False)
    department_email = models.EmailField(blank = True)
    department_phoneNumber = models.CharField(max_length=20, blank = True)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return (self.department_name) 

class AddUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, to_field='department_id', on_delete = models.CASCADE, null = True)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = True)

class Experimenters(models.Model):

    experimenter_id = models.AutoField(primary_key=True)
    experimenter_label =  models.CharField(max_length=10, unique=True, blank = False)
    experimenter_firstName = models.CharField(max_length=100, blank = True)
    experimenter_lastName = models.CharField(max_length=100, blank = True)
    experimenter_email = models.EmailField(blank = True)
    experimenter_phoneNumber = models.CharField(max_length=20, blank = True)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False)
    department_id = models.ForeignKey(Departments, to_field='department_id', on_delete = models.CASCADE, null = False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return (self.experimenter_label) 

class Devices(models.Model):

    device_id = models.AutoField(primary_key=True)
    device_label = models.CharField(max_length=100, unique=True, blank = False)    
    device_name = models.CharField(max_length=100, unique=True, blank = False)
    def __str__(self):
        return (self.device_label) 

class Donor(models.Model):
    SEX =   (
                (u"F",u"F"),
                (u"M",u"M"),
            )
    donor_id = models.AutoField(primary_key=True)
    donor_abbr = models.CharField(max_length=10, unique=True, blank = False)
    donor_sex = models.CharField(choices=SEX,max_length=120, blank = True, null=True)
    donor_age_years = models.IntegerField(blank = True, null=True)
    donor_age_months = models.IntegerField(blank = True, null=True)
    desensitization_note = models.CharField(max_length=255, blank = True)
    desensitization_allergen = models.CharField(max_length=255, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return (self.donor_abbr)

class Experiment(models.Model):

    bat_id = models.AutoField(primary_key=True)      
    bat_name = models.CharField(max_length=150, unique = True, blank = False)    
    date_of_measurement = models.DateField(blank = False)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False) 
    experimenter_id = models.ForeignKey(Experimenters, to_field='experimenter_id', on_delete = models.CASCADE, null = False)
    device_id = models.ForeignKey(Devices, to_field='device_id', on_delete = models.CASCADE, blank = True, null = True)
    beadExperiment = models.BooleanField()
    specialExperiment = models.BooleanField()
    specialNotes = models.TextField(max_length=250, blank=True, validators=[MaxLengthValidator(250)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return (self.bat_name)


class Panels(models.Model):
    panel_id = models.AutoField(primary_key=True)
    panel_name = models.CharField(max_length=15, blank = False, unique = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
       return str(self.panel_name)

class Analysis(models.Model):
    
    analysis_id = models.AutoField(primary_key=True)
    bat_id = models.ForeignKey(Experiment, to_field=('bat_id'), blank = True, null=True,  on_delete = models.CASCADE)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    panel_id = models.ForeignKey(Panels, to_field=('panel_id'), blank = True, null=True,  on_delete = models.CASCADE)
    condition = models.CharField(max_length=200, blank = True, null = True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)

class AnalysisMarkers(models.Model):
    ANALYSIS_TYPES = (
        (u"AutoBat", u'AutoBat'),
        (u"AutoGrat", u'AutoGrat'),
    )
    STATUS_TYPES = (
        (u"Waiting", u'Waiting'),
        (u"In Progress", u'In Progress'),
        (u"Ready", u'Ready'),
        (u"Error", u'Error'),
    )
    analysisMarker_id = models.AutoField(primary_key=True)
    chosen_z1 = models.CharField(max_length=20, blank = True, null = True)
    chosen_y1 = models.CharField(max_length=20, blank = True, null = True)
    chosen_z2 = models.CharField(max_length=100, blank = True, null = True)
    chosen_z2_2 = models.CharField(max_length=200, blank = True, null = True)
    analysis_date = models.DateField(blank = True, null=True)
    analysis_start_time = models.TimeField(blank = True, null=True)
    analysis_end_time = models.TimeField(blank = True, null=True)
    analysis_status = models.CharField(choices=STATUS_TYPES,max_length=120, blank = True, null=True)
    analysis_type = models.CharField(choices=ANALYSIS_TYPES,max_length=120, blank = True, null=True)
    analysis_type_version = models.CharField(max_length=12, blank = True, null=True)
    analysis_error = models.TextField(max_length=250, blank=True, validators=[MaxLengthValidator(250)])
    analysis_info_messages = models.TextField(max_length=1000, blank=True, validators=[MaxLengthValidator(1000)])
    analysis_manualThresholds = models.BooleanField(blank = True, null=True)
    analysis_id = models.ForeignKey(Analysis, to_field=('analysis_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)

    #analysis_id = models.CharField(max_length=20, blank = True, null = True)


class AnalysisThresholds(models.Model):
    thresHolds_id = models.AutoField(primary_key=True)
    X_Threshold = models.FloatField(blank = True, null = True)
    Y_Threshold = models.FloatField(blank = True, null = True)
    Z2_1_Threshold = models.FloatField(blank = True, null = True)
    Z2_2_Threshold = models.FloatField(blank = True, null = True)
    Z2_3_Threshold = models.FloatField(blank = True, null = True)
    Z2_4_Threshold = models.FloatField(blank = True, null = True)
    analysisMarker_id = models.ForeignKey(AnalysisMarkers, to_field=('analysisMarker_id'), blank = True, null=True,  on_delete = models.CASCADE)


class AnalysisFiles(models.Model):
    FILES_TYPES = (
        (u"PNG", u'PNG'),
        (u"PDF", u'PDF'),
        (u"Excel", u'Excel'),
    )
    file_id = models.AutoField(primary_key=True)
    file_path = models.TextField(max_length=500, unique = True, blank = False)
    file_type = models.CharField(choices=FILES_TYPES,max_length=120, blank = True, null=True)
    analysisMarker_id = models.ForeignKey(AnalysisMarkers, to_field=('analysisMarker_id'), blank = True, null=True,  on_delete = models.CASCADE)


class ExperimentFiles(models.Model):
    CONTROL_TYPES = (
        (u"Negative control", u'Negative control'),
        (u"Primary Positive control", u'Primary Positive control'),
        (u"Secondary Positive control", u'Secondary Positive control'),
        (u"Unstained", u'Unstained'),
        (u"Allergen", u'Allergen'),
    )
    file_id = models.AutoField(primary_key=True)
    file_name = models.TextField(max_length=200, blank = True)
    file = models.FileField(max_length=300, blank=True, null=True)
    analysis_id = models.ForeignKey(Analysis, to_field=('analysis_id'), blank = True, null=True,  on_delete = models.CASCADE)
    allergen = models.CharField(max_length=100, blank = True, null = True)
    control=  models.CharField(choices=CONTROL_TYPES,max_length=120, blank = True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
       return str(self.file_name)

class AnalysisResults(models.Model):
    RESPONDER_TYPES = (
        (u"NA", u'NA'),
        (u"aIgE Responder", u'aIgE Responder'),
        (u"aIgE None_Responder", u'aIgE None_Responder'),
        (u"fMLP Responder", u'fMLP Responder'),
        (u"fMLP None_Responder", u'fMLP None_Responder'),
    )

    id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(ExperimentFiles, related_name='analysis_results', blank = True, null=True,  on_delete = models.CASCADE)
    zMarker = models.CharField(max_length=100, blank = True, null = True)
    debrisPerc = models.FloatField(blank = True, null = True)
    firstDoubPerc = models.FloatField(blank = True, null = True)
    secDoubPerc = models.FloatField(blank = True, null = True)
    redQ4 = models.FloatField(blank = True, null = True)
    result = models.CharField(max_length=20, blank = True, null = True)
    blackQ2 = models.FloatField(blank = True, null = True)
    blackQ3 = models.FloatField(blank = True, null = True)
    blackQ4 = models.FloatField(blank = True, null = True)
    zmeanQ4 = models.FloatField(blank = True, null = True)
    Z1_minQ4 = models.FloatField(blank = True, null = True)
    Z1_maxQ4 = models.FloatField(blank = True, null = True)
    msi_YQ4 = models.FloatField(blank = True, null = True)
    cellQ3 = models.FloatField(blank = True, null = True)
    cellQ4 = models.FloatField(blank = True, null = True)
    responder = models.CharField(choices=RESPONDER_TYPES,max_length=120, blank = True, null=True)
    cellTotal = models.FloatField(blank = True, null = True)
    qualityMessages = models.TextField(max_length=250, blank=True, validators=[MaxLengthValidator(250)])
    plot_symbol = models.CharField(max_length=12, blank = True, null=True)
    analysisMarker_id = models.ForeignKey(AnalysisMarkers, to_field=('analysisMarker_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)


class FilesPlots(models.Model):
    plot_id = models.AutoField(primary_key=True)
    plot_path = models.TextField(max_length=500, unique = True, blank = False)
    file_id = models.ForeignKey(ExperimentFiles, to_field=('file_id'), blank = True, null=True,  on_delete = models.CASCADE)
    analysisMarker_id = models.ForeignKey(AnalysisMarkers, to_field=('analysisMarker_id'), blank = True, null=True,  on_delete = models.CASCADE)

class Channels(models.Model):
    channel_id = models.AutoField(primary_key=True)      
    pnn = models.CharField(max_length=50, blank = True)
    pns = models.CharField(max_length=50, blank = True)
    analysis_id = models.ForeignKey(Analysis, to_field=('analysis_id'), blank = True, null=True,  on_delete = models.CASCADE)

class MeanRawData(models.Model):    
    row_id = models.AutoField(primary_key=True) 
    labels = models.CharField(max_length=200, blank = True, null=True)
    values = models.CharField(max_length=200, blank = True, null=True)
    file_id = models.ForeignKey(ExperimentFiles, to_field=('file_id'), blank = True, null=True,  on_delete = models.CASCADE)

class MetaData(models.Model):    
    id = models.AutoField(primary_key=True)
    labels = models.CharField(max_length=200, blank = True)
    values = models.CharField(max_length=200, blank = True, null=True)
    file_id = models.ForeignKey(ExperimentFiles, to_field=('file_id'), blank = True, null=True,  on_delete = models.CASCADE)


class DonorTestBlood(models.Model):
    testBlood_id = models.AutoField(primary_key=True)
    gIgE = models.FloatField(blank = True, null = True)
    wheat_flour = models.FloatField(blank = True, null = True)
    gluten = models.FloatField(blank = True, null = True)
    gliadin = models.FloatField(blank = True, null = True)
    Tri_a_19 = models.FloatField(blank = True, null = True)
    Tri_a_14 = models.FloatField(blank = True, null = True)
    Tryptase = models.FloatField(blank = True, null = True)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)

class DonorTest_SPT(models.Model):
    spt_id = models.AutoField(primary_key=True)
    Histamine = models.FloatField(blank = True, null = True)
    NaCl = models.FloatField(blank = True, null = True)
    wheat_flour = models.FloatField(blank = True, null = True)
    wheat_gluten = models.FloatField(blank = True, null = True)
    birch = models.FloatField(blank = True, null = True)
    mugworth = models.FloatField(blank = True, null = True)
    timothy = models.FloatField(blank = True, null = True)
    house_dust_mite = models.FloatField(blank = True, null = True)
    cat = models.FloatField(blank = True, null = True)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)


class DonorTestOFC(models.Model):
    OFC_TYPES = (
        (u"positive", u'positive'),
        (u"negative", u'negative'),
        )
    ofc_id = models.AutoField(primary_key=True)
    donor_ofc = models.CharField(choices=OFC_TYPES,max_length=120, blank = True, null=True)
    gram_limit_ofc =  models.CharField(max_length=200, blank = True, null=True)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)

class DonorTestOFC_exercise(models.Model):
    OFC_TYPES = (
        (u"positive", u'positive'),
        (u"negative", u'negative'),
        )
    ofc_exercise_id = models.AutoField(primary_key=True)
    donor_ofc_exercise = models.CharField(choices=OFC_TYPES,max_length=120, blank = True, null=True)
    gram_limit_ofc_exercise = models.CharField(max_length=200, blank = True, null=True)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)


class ClinicalClass_Names(models.Model):
    clinicalClass_id = models.AutoField(primary_key=True)
    clinicalClass_name = models.CharField(max_length=150, unique = True, blank = False)
    def __str__(self):
        return (self.clinicalClass_name)

class DonorClinicalclass(models.Model):
    DonorClinicalClass_id = models.AutoField(primary_key=True)
    clinicalClass_id = models.ForeignKey(ClinicalClass_Names, to_field=('clinicalClass_id'), blank = True, null=True,  on_delete = models.CASCADE)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null = True)


