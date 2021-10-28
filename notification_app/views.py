from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from auth_app.models import Account
from post_app.models import ScreamModel, CommentModel
from notification_app.models import Notification


@login_required
def show_notify(request, user_id: int):
    """
    Gets all unread notifications from Notification model
    and filters only the ones linked to logged in user
    """
    my_user = Account.objects.get(id=user_id)
    notif_list = Notification.objects.filter(
        user_to_notify=my_user, read=False)[::-1]
    notif = Notification.objects.filter(
        user_to_notify=my_user, read=False)
    return render(request, 'notifications.html', {'notif_list': notif_list,
                                                  'notif': notif})


def NotifyMention(request, user_id: int, post_id: int):
    """
    Creates a Notification object when a user
    is tagged in a post
    """
    cur_user = Account.objects.get(id=request.user.id)
    notif_user = Account.objects.get(id=user_id)
    post = ScreamModel.objects.get(id=post_id)
    split = post.content.split()[:5]
    to_user = f"You've recieved a mention from {post.posted_by} that says: \
                        \'{' '.join(split).upper()}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=post.id,
        user_to_notify=notif_user,
        follower=False,
    )
    return


def NotifyComment(request, form_data, comment_model, post_id: int):
    cur_user = Account.objects.get(id=request.user.id)
    post = ScreamModel.objects.get(id=post_id)
    split = comment_model.content.split()[:5]
    split_content = post.content.split()[:5]
    to_user = f"You've recieved a comment on post \'{split_content[0]}\'... from: \
                        {cur_user} that says:\
                        \'{' '.join(split)}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        user_to_notify=post.posted_by,
        post_id=post.id,
        follower=False,
    )
    return


def NotifyLike(request, post_id: int):
    """
    Creates a Notification object when a users
    post recieves a like
    """
    cur_user = Account.objects.get(id=request.user.id)
    post = ScreamModel.objects.get(id=post_id)
    split = post.content.split()[:3]
    to_user = f"You've recieved a like on your post \'{' '.join(split).upper()}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=post.id,
        user_to_notify=post.posted_by,
        follower=False,
    )
    return


def NotifyLikeComment(request, comment_id: int, post_id: int):
    """
    Creates a Notification object when a users
    post recieves a like
    """
    cur_user = Account.objects.get(id=request.user.id)
    comment = CommentModel.objects.get(id=comment_id)
    post = ScreamModel.objects.get(id=post_id)
    split = comment.content.split()[:3]
    to_user = f"You've recieved a like on your comment \'{' '.join(split).upper()}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=post.id,
        user_to_notify=comment.comment_by,
        follower=False,
    )
    return


def NotifyDislike(request, post_id: int):
    """
    Creates a Notification object when a users
    post recieves a dislike
    """
    cur_user = Account.objects.get(id=request.user.id)
    post = ScreamModel.objects.get(id=post_id)
    split = post.content.split()[:3]
    to_user = f"You've recieved a dislike on your post \'{' '.join(split).upper()}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=post.id,
        user_to_notify=post.posted_by,
        follower=False,
    )
    return


def NotifyDislikeComment(request, comment_id: int, post_id: int):
    """
    Creates a Notification object when a users
    post recieves a dislike
    """
    cur_user = Account.objects.get(id=request.user.id)
    comment = CommentModel.objects.get(id=comment_id)
    post = ScreamModel.objects.get(id=post_id)
    split = comment.content.split()[:3]
    to_user = f"You've recieved a dislike on your comment \'{' '.join(split).upper()}...\'"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=post.id,
        user_to_notify=comment.comment_by,
        follower=False,
    )
    return


def NotifyFollow(request, user_id):
    """
    Creates a Notification object when a users
    post recieves a follow
    """
    cur_user = Account.objects.get(id=request.user.id)
    notif_user = Account.objects.get(id=user_id)
    follower = Account.objects.get(id=request.user.id)
    to_user = f"You've recieved a follow from: \
                    <a href='/profile/{follower.id}'>{follower.username}</a>"
    Notification.objects.create(
        message=to_user,
        made_by=cur_user,
        post_id=0,
        user_to_notify=notif_user,
        follower=True,
    )
    return


def mark_read(request, noti_id: int):
    """
    Will mark each individual notification as read
    or will mark them all as read depending on
    the button pressed
    """
    query = request.GET.get('data')
    # try:
    obj = Notification.objects.get(id=noti_id)
    # obj = Notification.objects.filter(
    #     user_to_notify=request.user.id)
    # each.read = True
    # each.save()
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if obj.DoesNotExist and query == 'read':
        for each in obj:
            print(each)
            # each.read = True
            # each.save()
            # return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # except Notification.DoesNotExist:
    #     messages.info(request, "Error deleting notification!")
    #     return render(request, 'notifications.html')
