# Generated by Django 3.1.14 on 2022-12-21 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0029_auto_20221222_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualnetwork',
            name='min_disk',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='virtualnetwork',
            name='min_ram',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='virtualnetwork',
            name='size',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='virtualnetwork',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='virtualnetwork',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
