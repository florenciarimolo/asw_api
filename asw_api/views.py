# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.contrib.auth.models import User
from django.db import OperationalError
from django.http import Http404, HttpResponseForbidden
from rest_framework import generics
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments
from asw_api.serializers import IssueSerializer, UserSerializer, CommentSerializer
from rest_extensions import generics as genericsx


def has_update_or_destroy_object_permission(request, obj):
    if request.user.is_authenticated:
        return obj.owner.username == request.user.username

    token = request.META['HTTP_AUTHORIZATION'].replace('Token ', '')
    owner_id = obj.owner.id
    owner_token_value = Token.objects.get(user_id=owner_id).key
    return token == owner_token_value


class Index(views.APIView):
    def get(self, request, format=None):
        data = OrderedDict((
            ('users', reverse('users-list', request=request, format=format)),
            ('issues', reverse('issues-list', request=request, format=format)),
        ))
        return Response(data, )


class UsersList(generics.ListAPIView):
    try:
        all_usernames = [u.username for u in User.objects.all() if u.username != 'admin']
        queryset = User.objects.filter(username__in=all_usernames)
    except OperationalError:
        pass
    serializer_class = UserSerializer


class UserDetail(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user, many=False)
            response = serializer.data
            return Response(response, )
        except User.DoesNotExist:
            raise Http404


class IssuesList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IssueDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer

    def put(self, request, *args, **kwargs):
        issue = Issues.objects.get(id=self.kwargs.get('pk'))
        print(issue.owner.username)
        if has_update_or_destroy_object_permission(request, issue):
            return self.update(request, *args, **kwargs)
        raise HttpResponseForbidden

    def delete(self, request, *args, **kwargs):
        issue = Issues.objects.get(id=self.kwargs.get('pk'))
        print(issue.owner.username)
        if has_update_or_destroy_object_permission(request, issue):
            return self.destroy(request, *args, **kwargs)
        raise HttpResponseForbidden


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Comments.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.filter(id=issue_id)[0]
        serializer.save(owner=self.request.user, issue=issue)


class CommentDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def put(self, request, *args, **kwargs):
        comment = Comments.objects.get(id=self.kwargs.get('pk'))
        if has_update_or_destroy_object_permission(request, comment):
            return self.update(request, *args, **kwargs)
        raise HttpResponseForbidden

    def delete(self, request, *args, **kwargs):
        comment = Comments.objects.get(id=self.kwargs.get('pk'))
        if has_update_or_destroy_object_permission(request, comment):
            return self.destroy(request, *args, **kwargs)
        raise HttpResponseForbidden
