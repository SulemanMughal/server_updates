# Generated by Django 3.1.14 on 2022-12-14 07:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master_app', '0009_auto_20221214_0208'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assignedstudents',
            unique_together={('course', 'student')},
        ),
    ]
