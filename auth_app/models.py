from django.db import models
from django.conf import settings
from djongo.storage import GridFSStorage
from django_countries.fields import CountryField


from django.contrib.auth.models import AbstractUser

pimg = '../static/images/profile_img.png'
# grid_fs_storage = GridFSStorage(collection='profile_images', base_url=''.join([
#                                 settings.BASE_URL, 'profile_images/']))


class Account(AbstractUser):
    bio = models.TextField(max_length=250, blank=True)
    profile_image = models.ImageField(
        default=pimg, upload_to='profile_images/',
        blank=True)
    date_of_birth = models.DateField(
        auto_now=False, default='1990-01-01')
    header = models.CharField(max_length=80, default="A 'lil sum sum")
    country = CountryField()
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
