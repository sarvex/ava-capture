# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-07 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_farmnode_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmjob',
            name='priority',
            field=models.IntegerField(default=50),
        ),
    ]