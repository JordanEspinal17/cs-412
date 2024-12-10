# Generated by Django 5.1.3 on 2024-12-09 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcam', '0004_coachfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('score', models.FloatField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rankings', to='webcam.uploadedvideo')),
            ],
        ),
    ]