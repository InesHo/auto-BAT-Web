# Generated by Django 3.2.8 on 2023-12-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0026_analysisresults_cellq3'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='condition',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
