# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asw_api', '0005_auto_20171130_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuesVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_id', models.ForeignKey(to='asw_api.Issues')),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ('issue_id',),
            },
        ),
        migrations.CreateModel(
            name='IssuesWaches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_id', models.ForeignKey(to='asw_api.Issues')),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'ordering': ('issue_id',),
            },
        ),
    ]
