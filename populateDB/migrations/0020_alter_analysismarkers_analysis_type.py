# Generated by Django 3.2.8 on 2023-09-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0019_auto_20230829_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysismarkers',
            name='analysis_type',
            field=models.CharField(blank=True, choices=[('AutoBat', 'AutoBat'), ('AutoGrat', 'AutoGrat')], max_length=120, null=True),
        ),
    ]
