# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-04 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0019_farmjob_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmnode',
            name='cpu_percent',
            field=models.FloatField(default=0.0),
        ),
    ]