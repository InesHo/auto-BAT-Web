# Generated by Django 3.2.8 on 2023-08-02 14:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('populateDB', '0010_remove_donorclass_clinical_donor_clinicalclass_id_old'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DonorClass_clinical',
            new_name='DonorClinicalClass',
        ),
        migrations.RenameField(
            model_name='donorclinicalclass',
            old_name='donor_class_id',
            new_name='classDonor_id',
        ),
        migrations.RenameField(
            model_name='donorclinicalclass',
            old_name='donor_clinicalClass_id',
            new_name='clinicalClass_id',
        ),
    ]
