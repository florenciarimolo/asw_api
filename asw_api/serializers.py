from rest_framework import serializers
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments
from django.contrib.auth.models import User

#from drf_hal_json.serializers import HalModelSerializer
#from drf_nested_fields.serializers import NestedFieldsSerializerMixin


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

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

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'image_url')


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()#HyperlinkedIdentityField(view_name='snippets:comment-detail', lookup_field='pk',)
    #owner = serializers.ReadOnlyField(source='owner.username')
    #issue = serializers.ReadOnlyField(source='issue.id')
    _links = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('comment-detail', request=request, format=format, kwargs=kwargs)

    def get__links(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        #kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        #url = reverse('comment-detail', request=request, format=format, kwargs=kwargs)
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
        fields = ('url', 'comment', '_links')#, 'owner', 'issue') #'__all__'


class IssueSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    #owner = serializers.ReadOnlyField(source='owner.username')
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
        #url = reverse('issue-detail', request=request, format=format, kwargs=kwargs)
        kwargss = {'username': obj.owner.username}
        url_owner = reverse('user-detail', request=request, format=format, kwargs=kwargss)
        url_comments = reverse('comments-list', request=request, format=format, kwargs=kwargs)
        return {
            #'self': {'href': url},
            'ea:owner': {'href': url_owner},
            'ea:comments': {'href': url_comments}
        }

    class Meta:
        model = Issues
        fields = ('url', 'title', 'kind', 'priority', 'status', 'votes', 'assignee', '_links', 'comments') #'owner', #'__all__'