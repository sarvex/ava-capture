# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-28 20:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20161128_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='name',
        ),
    ]