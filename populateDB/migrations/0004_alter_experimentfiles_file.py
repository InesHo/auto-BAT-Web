# Generated by Django 3.2.8 on 2022-12-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('populateDB', '0003_auto_20221207_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentfiles',
            name='file',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]
