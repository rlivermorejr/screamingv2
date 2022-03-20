from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

from django.contrib.auth.models import AbstractUser

pimg = '../static/images/profile_img.png'


class Account(AbstractUser):
    bio = models.TextField(max_length=250, default="I am blank!")
    profile_image = models.ImageField(
        default=pimg, upload_to='images/',
        blank=True)
    date_of_birth = models.DateField(
        auto_now=False, default='1990-01-01')
    header = models.CharField(max_length=15, editable=True, default="Noob")
    location = models.CharField(
        max_length=40, default="Armpit, CA")
    followers = models.ManyToManyField('self', symmetrical=False,
                                       related_name='auth_followers',
                                       blank=True)
    following = models.ManyToManyField('self', symmetrical=False,
                                       related_name='auth_following',
                                       blank=True)
    likes = models.ManyToManyField('self', symmetrical=False,
                                   blank=True,
                                   related_name='user_likes')
    dislikes = models.ManyToManyField('self', symmetrical=False,
                                      blank=True,
                                      related_name='user_dislikes')

    def __str__(self):
        return self.username
