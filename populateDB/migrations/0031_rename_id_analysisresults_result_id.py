# Generated by Django 3.2.8 on 2024-02-15 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0030_auto_20240123_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysisresults',
            old_name='id',
            new_name='result_id',
        ),
    ]
