# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0003_issues_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.TextField(blank=True, default='New'),
        ),
    ]
