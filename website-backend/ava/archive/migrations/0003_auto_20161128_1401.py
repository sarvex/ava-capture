# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-28 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_take_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='next_take',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='take',
            name='sequence',
            field=models.IntegerField(default=1),
        ),
    ]