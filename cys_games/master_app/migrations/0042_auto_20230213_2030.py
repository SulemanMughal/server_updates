# Generated by Django 3.1.14 on 2023-02-13 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0041_auto_20230213_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
