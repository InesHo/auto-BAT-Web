# Generated by Django 3.2.8 on 2023-11-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0025_alter_experimentfiles_control'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisresults',
            name='cellQ3',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
