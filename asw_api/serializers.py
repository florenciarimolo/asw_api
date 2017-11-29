from rest_framework import serializers
from rest_framework.reverse import reverse

from asw_api.models import *
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


class CommentsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')
    issue = serializers.ReadOnlyField(source='issue.id')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('comments-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Comments
        fields = '__all__'


class IssuesSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    comments = CommentsSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('issues-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Issues
        fields = '__all__'
