# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Issues(models.Model):
    title = models.TextField()
    kind = models.CharField(max_length=11)
    priority = models.CharField(max_length=8)
    status = models.TextField(default='New')
    votes = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True)
    assignee = models.ForeignKey(User, related_name='assignee', to_field='username', null=True)


class Comments(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, to_field='username')
    issue_id = models.ForeignKey(Issues, related_name='comments', to_field='id')


