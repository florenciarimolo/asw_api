from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from asw_api import views


urlpatterns = [
    url(r'^issues/$', views.IssuesList.as_view(), name='issues-list'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^issues/(?P<pk>[0-9]+)/comments/$', views.CommentsList.as_view(), name='comments-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/comments/(?P<pk>[0-9]+)$', views.CommentDetail.as_view(), name='comment-detail'),

    url(r'^issues/(?P<pk>[0-9]+)/vote/$', views.Vote.as_view(), name='vote'),
    url(r'^issues/(?P<pk>[0-9]+)/unvote/$', views.UnVote.as_view(), name='unvote'),
    url(r'^issues/(?P<pk>[0-9]+)/votes/$', views.IssueVotesList.as_view(), name='issue_votes-list'),

    url(r'^user/watch/(?P<pk>[0-9]+)/$', views.Watch.as_view(), name='watch'),
    url(r'^user/unwatch/(?P<pk>[0-9]+)/$', views.UnWatch.as_view(), name='unwatch'),
    url(r'^user/watches/$', views.UserWatchesList.as_view(), name='user_watches-list'),

    url(r'^issues/(?P<pk>[0-9]+)/attachments/$', views.AttachmentList.as_view(), name='attachment-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/attachments/(?P<pk>[0-9]+)$', views.AttachmentDetail.as_view(), name='attachment-detail'),
    url(r'^users/(?P<username>.+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/$', views.UsersList.as_view(), name='users-list'),

    url(r'^$', views.Index.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
