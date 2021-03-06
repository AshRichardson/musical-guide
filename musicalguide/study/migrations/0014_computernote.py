# Generated by Django 2.0.4 on 2018-05-13 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0013_note_interaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noteName', models.CharField(default='000', max_length=3)),
                ('startTime', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('interaction', models.CharField(default='echo', max_length=10)),
                ('participant', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='study.Participant')),
            ],
        ),
    ]
