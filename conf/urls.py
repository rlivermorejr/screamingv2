"""twitterclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from auth_app.views import CreateUser, index_page, login_user, logout_user
from post_app.views import (post_tweet, like_view, dislike_view,
                            view_post, CommentView)
from user_app.views import (EditUserProfile, get_user_profile, follow_user,
                            unfollow_user, followers, following,
                            user_likes, user_dislikes)
from notify_app.views import show_notify, mark_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    path('home/', post_tweet, name='main'),
    path('login/', login_user, name='login_page'),
    path('logout/', logout_user),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('like/<int:post_id>/', like_view),
    path('post/<int:post_id>/', view_post),
    path('profile/<int:user_id>/likes/', user_likes),
    path('profile/<int:user_id>/dislikes/', user_dislikes),
    path('mark_read/<int:noti_id>/', mark_read),
    path('profile/<int:user_id>/', get_user_profile, name='profile'),
    path('profile/<int:user_id>/edit/', EditUserProfile.as_view()),
    path('dislike/<int:post_id>/', dislike_view),
    path('profile/<int:user_id>/follow/', follow_user, name='follow'),
    path('profile/<int:user_id>/unfollow/', unfollow_user, name='unfollow'),
    path('profile/<int:user_id>/followers/', followers),
    path('profile/<int:user_id>/following/', following),
    path('notifications/<int:user_id>/', show_notify),
    path('comment/<int:post_id>/', CommentView.as_view(), name='post_comment')
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
handler404 = 'err_handler.views.handler403'
handler500 = 'err_handler.views.handler500'
handler403 = 'err_handler.views.handler404'
handler400 = 'err_handler.views.handler400'
