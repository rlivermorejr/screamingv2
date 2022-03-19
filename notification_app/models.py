from django.db import models
from auth_app.models import Account


class Notification(models.Model):
    message = models.TextField(max_length=100)
    made_by = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='from_user')
    user_to_notify = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='to_user')
    post_id = models.IntegerField(default=0)
    follower = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    rec_date = models.DateTimeField(auto_now=True, editable=False)

    # def get_count(self):
    #     """
    #     Gets the number of unread notifications
    #     """
    #     try:
    #         return Notification.objects.filter(read=False).count()
    #     except Notification.DoesNotExist:
    #         return 0
