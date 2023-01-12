# Generated by Django 3.1.14 on 2022-12-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0033_networkflagsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkflagsubmission',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('SUBMITTED', 'SUBMITTED')], default='PENDING', max_length=12),
        ),
    ]
