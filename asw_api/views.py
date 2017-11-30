# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.contrib.auth.models import User
from django.db import OperationalError
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_extensions import generics as genericsx
from asw_api.serializers import IssuesSerializer, UserSerializer, CommentsSerializer
from asw_api.models import Issues, Comments

FORBIDDEN_MESSAGE = {'details': 'You don\'t have permission to do this action using the credentials you supplied.'}


def has_object_permission(request, obj):
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    print('has_permission function')
    if request.method in permissions.SAFE_METHODS:
        print('safe method')
        if request.user.is_authenticated:
            return True
        token = request.META['HTTP_AUTHORIZATION'].replace('Token ', '')
        token_obj = Token.objects.get(key=token)  # check if the token exists
        if token_obj is None:
            return False
        return True
    else:
        print('not safe method')
        if request.user.is_authenticated:
            print(obj.owner.username)
            return obj.owner.username == request.user.username
        else:
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


class UsersDetail(generics.ListAPIView):

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


class IssuesDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer

    def put(self, request, *args, **kwargs):
        issue = Issues.objects.get(id=self.kwargs.get('pk'))
        print(issue.owner.username)
        if has_object_permission(request, issue):
            return self.update(request, *args, **kwargs)
        return Response(FORBIDDEN_MESSAGE, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        issue = Issues.objects.get(id=self.kwargs.get('pk'))
        print(issue.owner.username)
        if has_object_permission(request, issue):
            return self.destroy(request, *args, **kwargs)
        return Response(FORBIDDEN_MESSAGE, status=status.HTTP_403_FORBIDDEN)


class CommentsList(generics.ListCreateAPIView):

    serializer_class = CommentsSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Comments.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.filter(id=issue_id)[0]
        serializer.save(owner=self.request.user, issue=issue)


class CommentsDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def put(self, request, *args, **kwargs):
        comment = Comments.objects.get(id=self.kwargs.get('pk'))
        print(comment.owner.username)
        if has_object_permission(request, comment):
            return self.update(request, *args, **kwargs)
        return Response(FORBIDDEN_MESSAGE, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        comment = Comments.objects.get(id=self.kwargs.get('pk'))
        print(comment.owner.username)
        if has_object_permission(request, comment):
            return self.destroy(request, *args, **kwargs)
        return Response(FORBIDDEN_MESSAGE, status=status.HTTP_403_FORBIDDEN)
