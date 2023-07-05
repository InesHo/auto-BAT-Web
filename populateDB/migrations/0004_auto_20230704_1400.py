# Generated by Django 3.2.8 on 2023-07-04 14:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0003_donorclass_clinical_donor_clinicalclass_id_old'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysisresults',
            old_name='msi_Y',
            new_name='Z1_maxQ4',
        ),
        migrations.RenameField(
            model_name='analysisresults',
            old_name='z1_max',
            new_name='Z1_minQ4',
        ),
        migrations.RenameField(
            model_name='analysisresults',
            old_name='z1_min',
            new_name='cellTotal',
        ),
        migrations.AddField(
            model_name='analysisresults',
            name='debrisPerc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analysisresults',
            name='firstDoubPerc',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analysisresults',
            name='msi_YQ4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analysisresults',
            name='qualityMessages',
            field=models.TextField(blank=True, max_length=250, validators=[django.core.validators.MaxLengthValidator(250)]),
        ),
        migrations.AddField(
            model_name='analysisresults',
            name='secDoubPerc',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
