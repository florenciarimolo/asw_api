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
    status = models.TextField(blank=True) #default='New'
    assignee = models.ForeignKey(User, related_name='assignee', to_field='username', null=True)
    owner = models.ForeignKey(User, related_name='owner', to_field='username', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    comment = models.TextField()
    owner = models.ForeignKey(User, to_field='username')
    issue = models.ForeignKey(Issues, related_name='comments', to_field='id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, to_field='username')
    issue = models.ForeignKey(Issues, related_name='attachments', to_field='id')
    datafile = models.FileField(upload_to='downloads/')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class IssuesVotes(models.Model):
    issue_id = models.ForeignKey(Issues, to_field='id')
    username = models.ForeignKey(User, to_field='username')
    index_together = ["issue_id", "username"]

    class Meta:
        unique_together = (("issue_id", "username"),)
        ordering = ('issue_id',)


class IssuesWaches(models.Model):
    issue_id = models.ForeignKey(Issues, to_field='id')
    username = models.ForeignKey(User, to_field='username')
    index_together = ["issue_id", "username"]

    class Meta:
        unique_together = ("issue_id", "username",)
        ordering = ('issue_id',)
