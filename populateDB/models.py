from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Institutes(models.Model):

    institute_id = models.AutoField(primary_key=True)      
    institute_shortName = models.CharField(max_length=15, blank = False, unique = True)     
    institute_name = models.CharField(max_length=150, blank = True)    
    institute_address = models.CharField(max_length=150,  blank = True)  
    institute_email = models.EmailField(blank = True)
    institute_phoneNumber = models.CharField(max_length=20, blank = True) 
           
    class Meta:
        db_table = "populateDB_institutes"
    def __str__(self):
        return (self.institute_shortName) 

class Departments(models.Model):

    department_id = models.AutoField(primary_key=True)      
    department_name = models.CharField(max_length=150, unique=True, blank = False)
    department_email = models.EmailField(blank = True)
    department_phoneNumber = models.CharField(max_length=20, blank = True)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False)
          
    class Meta:
        db_table = "populateDB_departments"
    def __str__(self):
        return (self.department_name) 

class Experimenters(models.Model):

    experimenter_id = models.AutoField(primary_key=True)
    experimenter_label =  models.CharField(max_length=10, unique=True, blank = False)
    experimenter_firstName = models.CharField(max_length=100, blank = True)
    experimenter_lastName = models.CharField(max_length=100, blank = True)
    experimenter_email = models.EmailField(blank = True)
    experimenter_phoneNumber = models.CharField(max_length=20, blank = True)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False)
    department_id = models.ForeignKey(Departments, to_field='department_id', on_delete = models.CASCADE, null = False) 
          
    class Meta:
        db_table = "populateDB_experimenters"
    def __str__(self):
        return (self.experimenter_label) 


class Cytometers(models.Model):

    cytometer_id = models.AutoField(primary_key=True)      
    cytometername_short = models.CharField(max_length=15, unique=True, blank = False)
    cytometername_long = models.CharField(max_length=100, blank = False)
          
    class Meta:
        db_table = "populateDB_cytometers"
    def __str__(self):
        return (self.cytometername_short) 


class Devices(models.Model):

    device_id = models.AutoField(primary_key=True)      
    device_name = models.CharField(max_length=100, unique=True, blank = False)
          
    class Meta:
        db_table = "populateDB_devices"
    def __str__(self):
        return (self.device_name) 


class Markers(models.Model):

    marker_id = models.AutoField(primary_key=True)      
    marker_name = models.CharField(max_length=100, unique=True, blank = False)
          
    class Meta:
        db_table = "populateDB_markers"
    def __str__(self):
        return (self.marker_name) 


class Panels(models.Model):

    panel_id = models.AutoField(primary_key=True)      
    panel_name = models.CharField(max_length=100, unique=True, blank = False)
          
    class Meta:
        db_table = "populateDB_panels"
    def __str__(self):
        return (self.panel_name) 


class Donor(models.Model):

    donor_id = models.AutoField(primary_key=True)
    donor_abbr = models.CharField(max_length=10, unique=True, blank = False)
    desensitization_note = models.CharField(max_length=255, blank = True)
    desensitization_allergen = models.CharField(max_length=255, blank = True)
        
    class Meta:
        db_table = "populateDB_donors"
    def __str__(self):
        return (self.donor_abbr)

class Experiment(models.Model):

    bat_id = models.AutoField(primary_key=True)      
    bat_name = models.CharField(max_length=150, unique = True, blank = False)    
    date_of_measurement = models.DateField(blank = False)
    institute_id = models.ForeignKey(Institutes, to_field='institute_id', on_delete = models.CASCADE, null = False) 
    experimenter_id = models.ForeignKey(Experimenters, to_field='experimenter_id', on_delete = models.CASCADE, null = False)
    cytometer_id = models.ForeignKey(Cytometers, to_field='cytometer_id', on_delete = models.CASCADE, null = False)
    device_id = models.ForeignKey(Devices, to_field='device_id', on_delete = models.CASCADE, null = False)
    marker_id = models.ForeignKey(Markers, to_field='marker_id', on_delete = models.CASCADE, null = False)
    beadExperiment = models.BooleanField()
    specialExperiment = models.BooleanField()
    #specialNotes = models.CharField(max_length=255, blank = True) 
    specialNotes = models.TextField(max_length=250, blank=True,
                                   validators=[MaxLengthValidator(250)])
    
    class Meta:
        db_table = "populateDB_experiment"

    def __str__(self):
        return (self.bat_name)


class FileType(models.Model):

    type_id = models.AutoField(primary_key=True)      
    type_name = models.CharField(max_length=100, unique=True, blank = False)
          
    class Meta:
        db_table = "populateDB_fileType"
    def __str__(self):
        return (self.type_name)


class Post(models.Model):
    ...

class ExperimentFiles(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=50)
    image = models.FileField()
    bat_id = models.ForeignKey(Experiment, to_field=('bat_id'), blank = True, null=True,  on_delete = models.CASCADE)
    donor_id = models.ForeignKey(Donor, to_field=('donor_id'), blank = True, null=True,  on_delete = models.CASCADE)
    panel_id = models.ForeignKey(Panels, to_field=('panel_id'), blank = True, null=True,  on_delete = models.CASCADE)
    type_id = models.ForeignKey(FileType, to_field=('type_id'), blank = True, null=True,  on_delete = models.CASCADE)
    class Meta:
        db_table = "populateDB_experimentFiles"
    def __str__(self):
        return (self.file_name)