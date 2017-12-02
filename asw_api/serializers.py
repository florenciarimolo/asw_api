from rest_framework import serializers
from rest_framework.reverse import reverse

from asw_api.models import Issues, Comments
from django.contrib.auth.models import User

from drf_hal_json.serializers import HalModelSerializer
from drf_nested_fields.serializers import NestedFieldsSerializerMixin


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
    url = serializers.SerializerMethodField()#HyperlinkedIdentityField(view_name='snippets:comments-detail', lookup_field='pk',)
    owner = serializers.ReadOnlyField(source='owner.username')
    issue = serializers.ReadOnlyField(source='issue.id')

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'issue_id': obj.issue_id}
        return reverse('comments-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Comments
        fields = '__all__' #('comment', 'owner', 'issue')


class IssueSerializer(HalModelSerializer):#, NestedFieldsSerializerMixin, serializers.ModelSerializer):
    #url = serializers.SerializerMethodField()#HyperlinkedIdentityField(view_name='snippets:issues-detail', lookup_field='pk',)
    #comments = CommentsSerializer(many=True, read_only=True)
    owner = serializers.HyperlinkedIdentityField(view_name='user-detail')#ReadOnlyField(source='owner.username')
    #comments = 'comments-list'

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('issues-detail', request=request, format=format, kwargs=kwargs)

    class Meta:
        model = Issues
        fields = ('title', 'kind', 'priority', 'status', 'votes', 'assignee', 'owner')#, 'comments') #'__all__'
        #nested_fields = {
        #'comments': (
        #        ['comment'],
        #        {
        #            'owner': (
        #                ['url', 'owner']
        #        )
        #        }
        #)
        #}