# Generated by Django 3.1.14 on 2022-12-13 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0008_course_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_approved',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
