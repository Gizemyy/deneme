from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from spaces.views import (space_create,
                          space_index,
                          follow_space,
                          space_question_create,
                          space_detail,
                          space_question_detail,
                          space_question_delete,
                          space_question_update,
                          upvote_question,
                          downvote_question
                          )
app_name = "space"
urlpatterns = [
    url(r'^create/', space_create, name='create'),
    url(r'^spacelist/$', space_index, name='listspace'),
    url(r'^follow/(?P<slug>[\w-]+)$', follow_space, name='follow'),
    url(r'^detail/(?P<slug>[\w-]+)$', space_detail, name='spacedetail'),
    url(r'^upvote/(?P<slug>[\w-]+)/$', upvote_question, name='upvote'),
    url(r'^downvote/(?P<slug>[\w-]+)/$', downvote_question, name='downvote'),
    url(r'^qdetail/(?P<slug>[\w-]+)', space_question_detail, name='detail'),
    url(r'^update/(?P<slug>[\w-]+)', space_question_update, name="update"),
    url(r'^delete/(?P<slug>[\w-]+)', space_question_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)', space_question_create, name='askinspace'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
