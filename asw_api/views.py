# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db import OperationalError
from django.http import HttpResponse
from django.http import Http404, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework import views
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_extensions import generics as genericsx
from rest_framework.parsers import FormParser, MultiPartParser
from asw_api.serializers import IssueSerializer, UserSerializer, CommentSerializer, AttachmentSerializer
from asw_api.serializers import VoteSerializer, UnVoteSerializer, IssueVotesSerializer
from asw_api.serializers import WatchSerializer, UnWatchSerializer, UserWatchesSerializer
from asw_api.models import Issues, Comments, IssuesVotes, IssuesWaches, Attachment


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


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        queryset = User.objects.filter(username=username)
        return queryset


class IssuesList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('kind', 'priority', 'status', 'assignee')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status='New')


class IssueDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer

    def put(self, request, *args, **kwargs):
        issue = self.get_issue()
        if has_update_or_destroy_object_permission(request, issue):
            return self.update(request, *args, **kwargs)
        raise HttpResponseForbidden

    def delete(self, request, *args, **kwargs):
        issue = self.get_issue()
        if has_update_or_destroy_object_permission(request, issue):
            return self.destroy(request, *args, **kwargs)
        raise HttpResponseForbidden

    def get_issue(self):
        try:
            issue = Issues.objects.get(id=self.kwargs.get('pk'))
        except Issues.DoesNotExist:
            raise Http404
        return issue


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        try:
            Issues.objects.get(id=issue_id)
        except Issues.DoesNotExist:
            raise Http404
        return Comments.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.filter(id=issue_id)[0]
        serializer.save(owner=self.request.user, issue=issue)


class CommentDetail(genericsx.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get_comment(self):
        try:
            q1 = Q(id=self.kwargs.get('pk'))
            q2 = Q(issue_id=self.kwargs.get('issue_id'))
            comment = Comments.objects.get(q1 & q2)
        except Comments.DoesNotExist:
            raise Http404
        return comment

    def get(self, request, *args, **kwargs):
        try:
            q1 = Q(id=self.kwargs.get('pk'))
            q2 = Q(issue_id=self.kwargs.get('issue_id'))
            Comments.objects.get(q1 & q2)
        except Comments.DoesNotExist:
            raise Http404
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        comment = self.get_comment()
        if has_update_or_destroy_object_permission(request, comment):
            return self.update(request, *args, **kwargs)
        raise HttpResponseForbidden

    def delete(self, request, *args, **kwargs):
        comment = self.get_comment()
        if has_update_or_destroy_object_permission(request, comment):
            return self.destroy(request, *args, **kwargs)
        raise HttpResponseForbidden


class Vote(generics.CreateAPIView):
    # TODO 404 si la issue no existe
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.get(id=issue_id)
        username = self.request.user
        try:
            q1 = Q(issue_id=issue_id)
            q2 = Q(username=username)
            IssuesVotes.objects.get(q1 & q2)
            data = {'detail': 'Issue already voted.'}
            return Response(data, status=208)
        except ObjectDoesNotExist:
            IssuesVotes.objects.create(issue_id=issue, username=username)
            data = {'detail': 'Issue voted correctly.'}
            return Response(data, status=status.HTTP_201_CREATED)


class UnVote(generics.DestroyAPIView):
    # TODO 404 si la issue no existe
    serializer_class = UnVoteSerializer

    def delete(self, request, *args, **kwargs):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.get(id=issue_id)
        username = self.request.user
        try:
            q1 = Q(issue_id=issue_id)
            q2 = Q(username=username)
            IssuesVotes.objects.get(q1 & q2).delete()
            data = {'detail': 'Issue unvoted correctly.'}
            return Response(data, status=204)
        except ObjectDoesNotExist:
            data = {'detail': 'Issue already unvoted.'}
            return Response(data, status=208)


class IssueVotesList(generics.ListAPIView):
    # TODO 404 si la issue no existe
    serializer_class = IssueVotesSerializer
    queryset = IssuesWaches.objects.all()

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return IssuesVotes.objects.filter(issue_id=issue_id)


class Watch(generics.CreateAPIView):
    # TODO 404 si la issue no existe
    serializer_class = WatchSerializer

    def create(self, request, *args, **kwargs):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.get(id=issue_id)
        username = self.request.user
        try:
            q1 = Q(issue_id=issue_id)
            q2 = Q(username=username)
            IssuesWaches.objects.get(q1 & q2)
            data = {'detail': 'Issue already watched.'}
            return Response(data, status=208)
        except ObjectDoesNotExist:
            IssuesWaches.objects.create(issue_id=issue, username=username)
            data = {'detail': 'Issue watched correctly.'}
            return Response(data, status=status.HTTP_201_CREATED)


class UnWatch(generics.DestroyAPIView):
    # TODO 404 si la issue no existe
    serializer_class = UnWatchSerializer

    def delete(self, request, *args, **kwargs):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.get(id=issue_id)
        username = self.request.user
        try:
            q1 = Q(issue_id=issue_id)
            q2 = Q(username=username)
            IssuesWaches.objects.get(q1 & q2).delete()
            data = {'detail': 'Issue unwatched correctly.'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            data = {'detail': 'Issue already unwatched.'}
            return Response(data, status=208)


class UserWatchesList(generics.ListAPIView):
    serializer_class = UserWatchesSerializer
    queryset = IssuesWaches.objects.all()

    def get_queryset(self):
        username = self.request.user
        return IssuesWaches.objects.filter(username=username)


class AttachmentList(generics.ListCreateAPIView):
    # TODO 404 si la issue no existe
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_queryset(self):
        issue_id = self.kwargs.get('pk')
        return Attachment.objects.filter(issue=issue_id)

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('pk')
        issue = Issues.objects.get(id=issue_id)
        serializer.save(owner=self.request.user,
                        datafile=self.request.data.get('datafile'),
                        issue=issue)


class AttachmentDetail(generics.RetrieveDestroyAPIView):
    # TODO 404 si la issue o el attachment no existen
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def delete(self, request, *args, **kwargs):
        attachment = Attachment.objects.get(id=self.kwargs.get('pk'))
        if has_update_or_destroy_object_permission(request, attachment):
            return self.destroy(request, *args, **kwargs)
        return Response(HttpResponseForbidden, )
