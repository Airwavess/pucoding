# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-12 07:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeanringClub',
            fields=[
                ('lc_id', models.AutoField(primary_key=True, serialize=False)),
                ('lc_name', models.TextField()),
                ('lc_TA', models.TextField()),
                ('lc_teacher', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sc_week', models.TextField()),
                ('sc_num_of_cpl', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('st_id', models.TextField(primary_key=True, serialize=False)),
                ('st_name', models.TextField()),
                ('st_class', models.TextField()),
                ('lc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.LeanringClub')),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='st_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Student'),
        ),
    ]
