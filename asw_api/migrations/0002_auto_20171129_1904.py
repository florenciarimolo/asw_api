# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 19:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='issue_id',
            new_name='issue',
        ),
    ]
