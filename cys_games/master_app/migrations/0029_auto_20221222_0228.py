# Generated by Django 3.1.14 on 2022-12-21 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0028_auto_20221222_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualnetwork',
            name='operating_system',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='virtualnetwork',
            name='scenarios',
            field=models.CharField(default='1', max_length=200),
        ),
    ]
