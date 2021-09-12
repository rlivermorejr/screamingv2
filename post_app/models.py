from django.db import models
from django.utils import timezone
import math
import datetime
import time

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

    # @register.filter
    # def duration(td):
    #     total_seconds = int(td.total_seconds())
    #     hours = total_seconds // 3600
    #     minutes = (total_seconds % 3600) // 60

    #     return '{} hours {} min'.format(hours, minutes)

    def elapsed(self):
        seconds = self.creation_time.timestamp()
        dt = time.time()
        diff = dt - seconds
        diff_time = datetime.timedelta(seconds=diff)
        ts = int(diff_time.total_seconds())
        if ts < 3600:
            minutes = (ts % 3600) // 60
            return "%d Minutes ago" % (minutes)
        if diff_time.days > 0:
            return "%d Days ago" % (diff_time.days)
        if diff_time.days == 0:
            rounded = (math.ceil(ts))
            hours = rounded // 3600
            return "%d Hours ago" % (hours)

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
