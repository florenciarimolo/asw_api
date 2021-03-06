# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 11:23
from __future__ import unicode_literals

import asw_api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0011_merge_20171210_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='kind',
            field=models.CharField(max_length=11, validators=[asw_api.models.validate_kind]),
        ),
        migrations.AlterField(
            model_name='issues',
            name='priority',
            field=models.CharField(max_length=8, validators=[asw_api.models.validate_priority]),
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.TextField(blank=True, validators=[asw_api.models.validate_status]),
        ),
    ]
