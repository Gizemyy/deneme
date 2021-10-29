from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from ask.views import (question_create,
                       question_detail,
                       question_index,
                       profile_questions_list,
                       upvote_question,
                       downvote_question,
                       question_delete,
                       question_update)

app_name = "ask"
urlpatterns = [
    url(r'^home/$', question_index, name="home"),
    url(r'^myquestions/$', profile_questions_list, name="myquestions"),
    url(r'^create/$', question_create, name='create'),
    url(r'^upvote/(?P<slug>[\w-]+)/$', upvote_question, name='upvote'),
    url(r'^downvote/(?P<slug>[\w-]+)/$', downvote_question, name='downvote'),
    url(r'^(?P<slug>[\w-]+)/$', question_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', question_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/delete/$', question_delete, name='delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

