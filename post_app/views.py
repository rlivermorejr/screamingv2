from django.shortcuts import (render, HttpResponseRedirect,
                              reverse)
from django.contrib import messages
from django.views import View

from auth_app.models import Account
from post_app.models import ScreamModel, CommentModel
from post_app.forms import ScreamForm, CommentForm
from notification_app.views import (
    NotifyLike, NotifyDislike, NotifyMention, NotifyComment,
    NotifyDislikeComment, NotifyLikeComment)
from notification_app.models import Notification


def view_post(request, post_id: int):
    """
    Displays a single post
    """
    comment_form = CommentForm()
    temp = 'detail_pages/single_post.html'
    try:
        post = ScreamModel.objects.get(id=post_id)
        cur_user = Account.objects.get(id=request.user.id)
        comments = CommentModel.objects.filter(orig_post=post)
        notif = Notification.objects.filter(
            user_to_notify=cur_user, read=False)
        return render(request, temp, {'post': post,
                                      'comment': comments,
                                      'comment_form': comment_form,
                                      'notif': notif})
    except Exception as e:
        print(e)
        return render(request, temp, {'post': post,
                                      'comment_form': comment_form})


def like_view(request, post_id: int):
    """
    Links the user that clicks the like button to
    the Tweet object and then calls the
    corresponding notify function. This is done for
    future implementation of being able to view all
    of a users likes
    """
    post = ScreamModel.objects.get(id=post_id)
    cur_user = Account.objects.get(id=request.user.id)
    if cur_user in post.likes.all():
        post.likes.remove(cur_user)
        post.save()
    else:
        post.likes.add(cur_user)
        if cur_user in post.dislikes.all():
            post.dislikes.remove(cur_user)
            post.save()
        post.save()
        NotifyLike(request, post_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def like_comment(request, post_id: int, comment_id: int):
    """
    Links the user that clicks the like button to
    the Tweet object and then calls the
    corresponding notify function. This is done for
    future implementation of being able to view all
    of a users likes
    """
    comment = CommentModel.objects.get(id=comment_id)
    cur_user = Account.objects.get(id=request.user.id)
    if cur_user in comment.likes.all():
        comment.likes.remove(cur_user)
        comment.save()
    else:
        comment.likes.add(cur_user)
        if cur_user in comment.dislikes.all():
            comment.dislikes.remove(cur_user)
            comment.save()
        comment.save()
        NotifyLikeComment(request, comment_id, post_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def dislike_view(request, post_id: int):
    """
    Links the user that clicks the dislike button to
    the Tweet object and then calls the
    corresponding notify function. This is done for
    future implementation of being able to view all
    of a users dislikes
    """
    post = ScreamModel.objects.get(id=post_id)
    cur_user = Account.objects.get(id=request.user.id)
    if cur_user in post.dislikes.all():
        post.dislikes.remove(cur_user)
        post.save()
    else:
        post.dislikes.add(cur_user)
        if cur_user in post.likes.all():
            post.likes.remove(cur_user)
            post.save()
        post.save()
        NotifyDislike(request, post_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def dislike_comment(request, post_id: int, comment_id: int):
    """
    Links the user that clicks the dislike button to
    the Tweet object and then calls the
    corresponding notify function. This is done for
    future implementation of being able to view all
    of a users dislikes
    """
    comment = CommentModel.objects.get(id=comment_id)
    cur_user = Account.objects.get(id=request.user.id)
    if cur_user in comment.dislikes.all():
        comment.dislikes.remove(cur_user)
        comment.save()
    else:
        comment.dislikes.add(cur_user)
        if cur_user in comment.likes.all():
            comment.likes.remove(cur_user)
            comment.save()
        comment.save()
        NotifyDislikeComment(request, comment_id, post_id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_comment(request, comment_id: int):
    comment = CommentModel.objects.get(id=comment_id)
    cur_user = Account.objects.get(id=request.user.id)
    if comment.comment_by.username == cur_user.username:
        comment.delete()
        comment.save()
    else:
        messages.info(request, "Cannot delete comment!")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def post_tweet(request):
    """
    If statement to redirect to login page if
    no user is logged in. If user is logged in
    it displays all posts, most recent first,
    then waits for post method to create a new
    post. Also runs mention function to check
    for a mention in the post
    """
    if request.method == 'POST':
        form = ScreamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            obj = ScreamModel.objects.create(
                content=data['content'].upper(),
                posted_by=request.user
            )
            mention(request, data, obj)
            return HttpResponseRedirect(reverse('main'))
    post_tweet = ScreamForm()
    comment_form = CommentForm()
    tweets = ScreamModel.objects.all()[::-1]
    try:
        cur_user = Account.objects.get(id=request.user.id)
        notif = Notification.objects.filter(
            user_to_notify=cur_user, read=False)
    except Account.DoesNotExist:
        return render(request, 'main.html', {'post_tweet': post_tweet,
                                             'tweets': tweets})
    return render(request, 'main.html', {'post_tweet': post_tweet,
                                         'tweets': tweets,
                                         'notif': notif,
                                         'comment_form': comment_form})


def mention(request, data, obj):
    """
    Mention function checks for @
    and if found, will get the word
    following symbol and then creates
    a link to that users profile embeded in the
    post itself. If the user does not exists
    a message will pop up on the homepage and
    that post is deleted
    """
    li = obj.content.split()
    post_id = obj.id
    for i in li:
        if i[0] == '@':
            try:
                st = i[1:]
                m_user = Account.objects.get(username=st)
                if m_user:
                    k = f"<a href='/profile/{m_user.id}'>{st}</a>"
                    obj.content = obj.content.replace(st, k)
                    obj.save()
                    NotifyMention(request, m_user.id, post_id)
            except Account.DoesNotExist:
                ScreamModel.delete(obj)
                messages.info(request, "This account does not exist!")
                return HttpResponseRedirect(reverse('main'))


class CommentView(View):
    def get(self, request, post_id: int):
        comment_form = CommentForm()
        cur_post = ScreamModel.objects.get(id=post_id)
        comment = CommentModel.objects.filter(orig_post=cur_post)
        return render(request, "main.html", {'comment_form': comment_form,
                                             'comment': comment})

    def post(self, request, post_id: int):
        cur_post = ScreamModel.objects.get(id=post_id)
        form = CommentForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            obj = CommentModel.objects.create(
                orig_post=cur_post,
                content=data['content'].upper(),
                comment_by=request.user,
            )
            cur_post.comments.add(obj)
            cur_post.save()
            NotifyComment(request, data, obj, cur_post.id)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
