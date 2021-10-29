from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import (login_view,
                            register_view,
                            logout_view,
                            profile_update,
                            profile_detail,
                            show_another_profile,
                            profile_following_space,
                            follow_profile)

app_name = "accounts"
urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^register/$', register_view, name="register"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^profile/edit/', profile_update, name="edit"),
    url(r'^profile/', profile_detail, name="profile"),
    url(r'^showprofile/(?P<id>[\w-]+)', show_another_profile, name="showprofile"),
    url(r'^profilefollowing/(?P<id>[\w-]+)', profile_following_space, name="profilefollowingspace"),
    url(r'^follow/(?P<id>[\w-]+)', follow_profile, name='followprofile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
