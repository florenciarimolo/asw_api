# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 17:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0008_auto_20171209_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issues',
            name='votes',
        ),
    ]
