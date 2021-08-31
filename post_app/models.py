from django.db import models
from django.utils import timezone

from auth_app.models import Account


class ScreamModel(models.Model):
    content = models.CharField(max_length=140)
    posted_by = models.ForeignKey(Account, on_delete=models.CASCADE,
                                  related_name='posted_by')
    likes = models.ManyToManyField(Account,
                                   related_name='liked_by',
                                   blank=True)
    dislikes = models.ManyToManyField(Account,
                                      related_name='disliked_by',
                                      blank=True)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)
    comments = models.ManyToManyField('CommentModel',
                                      blank=True,
                                      related_name='post_comments')

    # def elapsed(self):
    #     seconds = self.creation_time
    #     min, sec = divmod(seconds, 60)
    #     hour, min = divmod(min, 60)
    #     return seconds.second
    #     if hour == 1:
    #         return "%d hour ago", (hour)
    #     if hour > 1:
    #         return "%d hours ago", (hour)
    #     if hour == 0:
    #         return "%d minutes ago", (min)

    def __str__(self):
        return self.content


class CommentModel(models.Model):
    orig_post = models.ForeignKey(
        ScreamModel, related_name='original_post', on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(
        Account, related_name='comment_like', blank=True)
    dislikes = models.ManyToManyField(
        Account, related_name='comment_dislikes', blank=True)
    comment_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
