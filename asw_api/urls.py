from django.conf.urls import url

from asw_api import views

urlpatterns = [
    url(r'^issues/$', views.IssuesList.as_view(), name='issues-list'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssuesDetail.as_view(), name='issues-detail'),
    url(r'^issues/(?P<pk>[0-9]+)/comments/$', views.CommentsList.as_view(), name='comments-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/comments/(?P<pk>[0-9]+)$', views.CommentsDetail.as_view(), name='comments-detail'),
    url(r'^users/(?P<username>.+)$', views.UsersDetail.as_view(), name='user-detail'),
    url(r'^users/$', views.UsersList.as_view(), name='users-list'),
    url(r'^$', views.Index.as_view())
]
