import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from pytz import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments, IssuesVotes, IssuesWaches, Attachment


class UserSerializer(serializers.ModelSerializer):
    href = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    watches = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        imge_url = ''
        try:
            imge_url = obj.socialaccount_set.filter(provider='twitter')[0].extra_data['profile_image_url']
        except:
            pass
        return imge_url

    def get_watches(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        if request is not None and request.user and request.user.username == obj.username:
            return reverse('user-watches-list', request=request, format=format)
        return None

    def get_href(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'username': obj.username}
        return reverse('user-detail', request=request, format=format, kwargs=kwargs)

    def get_token(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        data = None
        if request is not None and request.user and request.user.username == obj.username:
            user_id = obj.id
            data = 'Token ' + Token.objects.get(user_id=user_id).key
        return data

    class Meta:
        model = User
        fields = ('href',
                  'username',
                  'first_name',
                  'last_name',
                  'image_url',
                  'watches',
                  'token')


class CommentSerializer(serializers.ModelSerializer):
    href = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.replace(tzinfo=timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.replace(tzinfo=timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')


    def get_href(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('comment-detail', request=request, format=format, kwargs=kwargs)

    def get__links(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargss = {'username': obj.owner.username}
        url_owner = reverse('user-detail', request=request, format=format, kwargs=kwargss)
        kwargsss = {'pk': obj.issue.id}
        url_issue = reverse('issue-detail', request=request, format=format, kwargs=kwargsss)
        return {
            'ea:owner': {'href': url_owner},
            'ea:issue': {'href': url_issue}
        }

    class Meta:
        model = Comments
        fields = ('href',
                  'id',
                  'comment',
                  'owner',
                  'created_at',
                  'updated_at',
                  '_links',)


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    issue = serializers.ReadOnlyField(source='issue.id')
    datafile = serializers.FileField(max_length=None, use_url=True)
    created = serializers.SerializerMethodField()

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d %H:%M:%S')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('attachment-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Attachment
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    href = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    attachments_url = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True, read_only=True)
    votes = serializers.SerializerMethodField()
    watchers = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()
    unvote = serializers.SerializerMethodField()
    watch = serializers.SerializerMethodField()
    unwatch = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_vote(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        if request is not None and request.user:
            try:
                q1 = Q(issue_id=obj.id)
                q2 = Q(username=request.user.username)
                IssuesVotes.objects.get(q1 & q2)
                return None
            except IssuesVotes.DoesNotExist:
                kwargs = {'pk': obj.id}
                return reverse('vote', request=request, format=format, kwargs=kwargs)
        return None

    def get_unvote(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        if request is not None and request.user:
            try:
                q1 = Q(issue_id=obj.id)
                q2 = Q(username=request.user.username)
                IssuesVotes.objects.get(q1 & q2)
                kwargs = {'pk': obj.id}
                return reverse('unvote', request=request, format=format, kwargs=kwargs)
            except IssuesVotes.DoesNotExist:
                return None

        return None

    def get_watch(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        if request is not None and request.user:
            try:
                q1 = Q(issue_id=obj.id)
                q2 = Q(username=request.user.username)
                IssuesWaches.objects.get(q1 & q2)
                return None
            except IssuesWaches.DoesNotExist:
                kwargs = {'pk': obj.id}
                return reverse('watch', request=request, format=format, kwargs=kwargs)
        return None

    def get_unwatch(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        if request is not None and request.user:
            try:
                q1 = Q(issue_id=obj.id)
                q2 = Q(username=request.user.username)
                IssuesWaches.objects.get(q1 & q2)
                kwargs = {'pk': obj.id}
                return reverse('unwatch', request=request, format=format, kwargs=kwargs)
            except IssuesWaches.DoesNotExist:
                return None
        return None

    def get_votes(self, obj):
        return IssuesVotes.objects.filter(issue_id=obj.id).count()

    def get_watchers(self, obj):
        return IssuesWaches.objects.filter(issue_id=obj.id).count()

    def get_href(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('issue-detail', request=request, format=format, kwargs=kwargs)

    def get_attachments_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('attachment-list', request=request, format=format, kwargs=kwargs)

    def get__links(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        kwargss = {'username': obj.owner.username}
        url_owner = reverse('user-detail', request=request, format=format, kwargs=kwargss)
        url_comments = reverse('comments-list', request=request, format=format, kwargs=kwargs)
        return {
            'ea:owner': {'href': url_owner},
            'ea:comments': {'href': url_comments}
        }

    class Meta:
        model = Issues
        fields = ('id',
                  'href',
                  'title',
                  'description',
                  'kind',
                  'priority',
                  'status',
                  'votes',
                  'vote',
                  'unvote',
                  'watchers',
                  'watch',
                  'unwatch',
                  'assignee',
                  'owner',
                  'created_at',
                  'updated_at',
                  '_links',
                  'comments',
                  'attachments_url',
                  'attachments',)


class VoteSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('vote', kwargs=kwargs)

    class Meta:
        model = IssuesVotes
        fields = ()


class UnVoteSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('unvote', kwargs=kwargs)

    class Meta:
        model = IssuesVotes
        fields = ()


class IssueVotesSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('issue_votes-list', kwargs=kwargs)

    class Meta:
        model = IssuesVotes
        fields = ('username',)


class WatchSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('watch', kwargs=kwargs)

    class Meta:
        model = IssuesWaches
        fields = ()


class UnWatchSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('unwatch', kwargs=kwargs)

    class Meta:
        model = IssuesWaches
        fields = ()


class UserWatchesSerializer(serializers.ModelSerializer):

    def get_url(self, obj):
        return reverse('user_watches-list')

    class Meta:
        model = IssuesWaches
        fields = ('issue_id',)
