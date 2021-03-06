# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-08 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asw_api', '0006_issuesvotes_issueswaches'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='issuesvotes',
            unique_together=set([('issue_id', 'username')]),
        ),
        migrations.AlterUniqueTogether(
            name='issueswaches',
            unique_together=set([('issue_id', 'username')]),
        ),
    ]
