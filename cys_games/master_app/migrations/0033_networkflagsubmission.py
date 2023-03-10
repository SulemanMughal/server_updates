# Generated by Django 3.1.14 on 2022-12-23 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master_app', '0032_networkflag'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkFlagSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_id', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('obtainedPoints', models.IntegerField(blank=True, default=0, null=True)),
                ('submittedAnswer', models.CharField(blank=True, default='', max_length=100)),
                ('attemptUsed', models.IntegerField(blank=True, default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_app.assignedstudents')),
            ],
        ),
    ]
