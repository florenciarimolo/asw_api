# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class Issues(models.Model):
    title = models.TextField()
    kind = models.CharField(max_length=11)
    priority = models.CharField(max_length=8)
    status = models.TextField(default='New', blank=True)
    votes = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True)
    assignee = models.ForeignKey(User, related_name='assignee', to_field='username', null=True)
    owner = models.ForeignKey(User, related_name='owner', to_field='username', null=True)


class Comments(models.Model):
    comment = models.TextField()
    owner = models.ForeignKey(User, to_field='username')
    issue = models.ForeignKey(Issues, related_name='comments', to_field='id')


class FileUploads(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='username')
    issue = models.ForeignKey(Issues, to_field='id')
    datafile = models.FileField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
