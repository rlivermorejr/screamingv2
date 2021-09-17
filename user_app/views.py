from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

from django.http import HttpResponseRedirect
from auth_app.models import Account
from notification_app.views import NotifyFollow
from notification_app.models import Notification
from post_app.models import ScreamModel
from post_app.forms import CommentForm
from user_app.forms import EditProfile


def get_user_profile(request, user_id: int):
    """
    Displays user profile and also checks
    for existing user in case you manually
    type the address in the url
    """
    try:
        account = Account.objects.get(id=user_id)
        try:
            cur_user = Account.objects.get(id=request.user.id)
            notif = Notification.objects.filter(
                user_to_notify=cur_user, read=False)
            posts = ScreamModel.objects.filter(posted_by=cur_user)[::-1]
            comment_form = CommentForm()
        except Account.DoesNotExist:
            return render(request, 'profile.html', {'account': account})
    except Account.DoesNotExist:
        messages.info(request, "This account does not exist!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'profile.html', {'account': account,
                                            'notif': notif,
                                            'posts': posts,
                                            'comment_form': comment_form})


@login_required
def follow_user(request, user_id: int):
    """
    Will check that you are not currently following
    the other user and will also check if
    the user is yourself
    """
    cur_user = Account.objects.get(id=request.user.id)
    follow = Account.objects.get(id=user_id)
    if follow.id == cur_user.id:
        messages.info(request, "You cannot follow yourself!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if not follow.followers.filter(username=cur_user.username).exists():
        cur_user.following.add(follow)
        cur_user.save()
        follow.followers.add(cur_user)
        follow.save()
        NotifyFollow(request, user_id)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You're already following this person!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def unfollow_user(request, user_id):
    """
    Makes sure you are actually following
    the other user. It will also check
    to make sure the other user is not
    yourself
    """
    cur_user = Account.objects.get(id=request.user.id)
    unfollow = Account.objects.get(id=user_id)
    if unfollow.id == cur_user.id:
        messages.info(request, "You're not following yourself!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if unfollow.followers.filter(username=cur_user.username).exists():
        cur_user.following.remove(unfollow)
        unfollow.followers.remove(cur_user)
        unfollow.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.info(request, "You're not following this person!")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def following(request, user_id: int):
    """
    Shows all of the users being followed
    by the user of the profile you are
    currently viewing
    """
    account = Account.objects.get(id=user_id)
    following = account.following.all()
    try:
        cur_user = Account.objects.get(id=request.user.id)
        notif = Notification.objects.filter(
            user_to_notify=cur_user, read=False)
    except Account.DoesNotExist:
        return render(request, 'detail_pages/list_follow.html', {'list': following})
    return render(request, 'detail_pages/list_follow.html', {'list': following,
                                                             'notif': notif})


def followers(request, user_id: int):
    """
    Shows all of the followers from the profile
    you are currently viewing
    """
    account = Account.objects.get(id=user_id)
    followers = account.followers.all()
    try:
        cur_user = Account.objects.get(id=request.user.id)
        notif = Notification.objects.filter(
            user_to_notify=cur_user, read=False)
    except Account.DoesNotExist:
        return render(request, 'detail_pages/list_follow.html', {'list': followers})
    return render(request, 'detail_pages/list_follow.html', {'list': followers,
                                                             'notif': notif})


def user_likes(request, user_id: int):
    account = Account.objects.get(id=user_id)
    likes = ScreamModel.objects.filter(likes=account)
    return render(request, 'detail_pages/list_likes.html', {'list': likes})


def user_dislikes(request, user_id: int):
    account = Account.objects.get(id=user_id)
    dislikes = ScreamModel.objects.filter(dislikes=account)
    return render(request, 'detail_pages/list_likes.html', {'list': dislikes})


class EditUserProfile(View):
    def get(self, request, user_id):
        cur_user = Account.objects.get(id=user_id)
        form = EditProfile(initial={
            'bio': cur_user.bio,
            'header': cur_user.header,
            'date_of_birth': cur_user.date_of_birth,
            'country': cur_user.country,
        })
        return render(request, 'forms/edit_profile.html', {'form': form})

    def post(self, request, user_id):
        cur_user = Account.objects.get(id=user_id)
        form = EditProfile(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            cur_user.bio = data['bio']
            cur_user.header = data['header']
            cur_user.date_of_birth = data['date_of_birth']
            cur_user.country = data['country']
            cur_user.save()
            return render(request, 'profile.html', {'account': cur_user})
        else:
            print(form.errors)
            messages.info(request, "Error in the form!")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])


# class ProfileImage(View):
#     def get(self, request, user_id):
#         cur_user = Account.objects.get(id=user_id)
#         form = ChangeProfileImage(initial={
#             'profile_image': cur_user.profile_image
#         })
#         return render(request, 'forms/gen_form.html', {'form': form})

#     def post(self, request, user_id):
#         cur_user = Account.objects.get(id=user_id)
#         form = ChangeProfileImage(request.POST, request.FILES)
#         print(form.errors)
#         if form.is_valid():
#             data = form.cleaned_data
#             cur_user.profile_image = data['profile_image']
#             cur_user.save()
#             return render(request, 'profile.html', {'account': cur_user})
#         else:
#             print(form.errors)
#             messages.info(request, "Error in the form!")
#             return HttpResponseRedirect(request.META['HTTP_REFERER'])
