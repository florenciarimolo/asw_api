from django.conf.urls import url

from asw_api import views

# url(r'^fileUploads/(?P<pk>[0-9]+)$', views.FileUploadDetail.as_view(), name='fileUploads-detail'),

urlpatterns = [
    url(r'^issues/$', views.IssuesList.as_view(), name='issues-list'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^issues/(?P<pk>[0-9]+)/comments/$', views.CommentsList.as_view(), name='comments-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/comments/(?P<pk>[0-9]+)$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^issues/(?P<pk>[0-9]+)/fileUploads/$', views.FileUploadsList.as_view(), name='fileUpload-list'),
    url(r'^issues/(?P<issue_id>[0-9]+)/fileUploads/(?P<pk>[0-9]+)$', views.FileUploadDetail.as_view(), name='fileUpload-detail'),
    url(r'^users/(?P<username>.+)$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^users/$', views.UsersList.as_view(), name='users-list'),
    url(r'^$', views.Index.as_view())
]