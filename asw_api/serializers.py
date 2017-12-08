from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        imge_url = ''
        try:
            imge_url = obj.socialaccount_set.filter(provider='twitter')[0].extra_data['profile_image_url']
        except:
            pass
        return imge_url

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'username': obj.username}
        return reverse('user-detail', request=request, format=format, kwargs=kwargs)

    def get_token(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        data = None
        if request.user and request.user.username == obj.username:
            user_id = obj.id
            data = Token.objects.get(user_id=user_id).key
        return data

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'image_url', 'token')


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()

    def get_url(self, obj):
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
        fields = ('url', 'comment', '_links')


class IssueSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    _links = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('issue-detail', request=request, format=format, kwargs=kwargs)

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
        fields = ('url', 'title', 'kind', 'priority', 'status', 'votes', 'assignee', '_links', 'comments')