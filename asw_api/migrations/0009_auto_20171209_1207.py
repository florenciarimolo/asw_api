# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0008_auto_20171207_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='datafile',
            field=models.FileField(upload_to='downloads/'),
        ),
    ]
