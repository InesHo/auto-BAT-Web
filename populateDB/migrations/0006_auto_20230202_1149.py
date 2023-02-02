# Generated by Django 3.2.8 on 2023-02-02 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0005_alter_analysismarkers_analysis_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysisfiles',
            name='analysisMarker_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.analysismarkers'),
        ),
        migrations.AlterField(
            model_name='analysismarkers',
            name='analysis_status',
            field=models.CharField(blank=True, choices=[('Waiting', 'Waiting'), ('In Progress', 'In Progress'), ('Ready', 'Ready')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='analysisresults',
            name='analysisMarker_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.analysismarkers'),
        ),
        migrations.AlterField(
            model_name='channels',
            name='analysis_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.analysis'),
        ),
        migrations.AlterField(
            model_name='experimentfiles',
            name='analysis_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.analysis'),
        ),
        migrations.AlterField(
            model_name='filesplots',
            name='file_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.experimentfiles'),
        ),
        migrations.AlterField(
            model_name='meanrawdata',
            name='file_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.experimentfiles'),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='file_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.experimentfiles'),
        ),
    ]
