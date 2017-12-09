from rest_framework import serializers
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments, IssuesVotes, IssuesWaches
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        imge_url = obj.socialaccount_set.filter(provider='twitter')[0].extra_data['profile_image_url']
        return imge_url

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'username': obj.username}
        return reverse('user-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'image_url')


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    issue = serializers.ReadOnlyField(source='issue.id')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('comment-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Comments
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('issue-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Issues
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        return reverse('vote-list', request=request, format=format)

    class Meta:
        model = IssuesVotes
        fields = '__all__'

class IssuesVotesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('issues_votes-list')

    class Meta:
        model = IssuesVotes
        fields = '__all__'

class IssueVotesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        kwargs = {'pk': obj.id}
        return reverse('issue_votes-list', kwargs=kwargs)

    class Meta:
        model = IssuesVotes
        fields = '__all__'

