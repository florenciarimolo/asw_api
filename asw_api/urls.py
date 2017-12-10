from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from asw_api import views


urlpatterns = [
    url(r'^issues/$', views.IssuesList.as_view(), name='issues-list'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^issues/(?P<pk>[0-9]+)/comments/$', views.CommentsList.as_view(), name='comments-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/comments/(?P<pk>[0-9]+)$', views.CommentDetail.as_view(), name='comment-detail'),

    url(r'^issues/(?P<pk>[0-9]+)/votes/(?P<username>.+)/$', views.Vote.as_view(), name='vote-list'),
    url(r'^issues/(?P<pk>[0-9]+)/votes/$', views.IssueVotesList.as_view(), name='issue_votes-list'),
    url(r'^issues/votes/$', views.IssuesVotesList.as_view(), name='issues_votes-list'),

    url(r'^users/(?P<username>.+)/watches/(?P<pk>[0-9]+)/$', views.Watch.as_view(), name='watch-list'),
    url(r'^users/(?P<username>.+)/watches/$', views.UserWatchesList.as_view(), name='user_watches-list'),
    url(r'^users/watches/$', views.IssuesWatchList.as_view(), name='issues_watch-list'),

    url(r'^issues/(?P<pk>[0-9]+)/attachments/$', views.AttachmentList.as_view(), name='attachment-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/attachments/(?P<pk>[0-9]+)$', views.AttachmentDetail.as_view(), name='attachment-detail'),
    url(r'^users/(?P<username>.+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/$', views.UsersList.as_view(), name='users-list'),

    url(r'^$', views.Index.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
