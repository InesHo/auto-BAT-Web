# Generated by Django 3.2.8 on 2024-01-23 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0029_auto_20240116_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysismarkers',
            name='chosen_y1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='analysismarkers',
            name='chosen_z1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
