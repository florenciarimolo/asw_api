# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.db import OperationalError
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from asw_api.models import *
from asw_api.serializers import *
from rest_framework import generics, viewsets
from rest_framework import views
from django.shortcuts import render


class Index(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = OrderedDict((
            ('users', reverse('users-list', request=request, format=format)),
            ('issues', reverse('issues-list', request=request, format=format)),
            ('comments', reverse('comments-list', request=request, format=format))
        ))
        return Response(data, )


class UsersList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    try:
        all_usernames = [u.username for u in User.objects.all() if u.username != 'admin']
        queryset = User.objects.filter(username__in=all_usernames)
    except OperationalError:
        pass
    serializer_class = UserSerializer


class UsersDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        kwargs = self.kwargs.get('username')
        user = User.objects.filter(username=kwargs)[0]
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class IssuesList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssuesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer


class CommentsList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentsSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Comments.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.filter(id=issue_id)[0]
        serializer.save(user=self.request.user, issue=issue)


class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
