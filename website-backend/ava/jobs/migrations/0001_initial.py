# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FarmNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=200)),
                ('machine_name', models.CharField(max_length=200)),
                ('last_seen', models.DateTimeField(auto_now_add=True, verbose_name='last seen')),
                ('online', models.BooleanField(default=False)),
            ],
        ),
    ]