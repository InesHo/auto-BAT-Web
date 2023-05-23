# Generated by Django 3.2.8 on 2023-05-23 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('populateDB', '0023_auto_20230523_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonorClass_clinical',
            fields=[
                ('donor_class_id', models.AutoField(primary_key=True, serialize=False)),
                ('donor_clinicalClass_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.clinicalclass_names')),
                ('donor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='populateDB.donor')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
