# Generated by Django 3.1.14 on 2022-12-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0018_auto_20221216_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursechallenge',
            name='points',
            field=models.IntegerField(blank=True, default=50),
        ),
    ]
