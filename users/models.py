from django.db import models
from django.contrib.auth.models import User
from core.models import *



class MetaProfile(models.Model):
    """
        Username allows saving temporary profiles
        of each user, for a faster internal search
    """
    full_name = models.CharField(max_length=355,blank=False)
    username = models.CharField(max_length=50,blank=False)
    image_url = models.URLField(blank=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
        @notice Profile class used for storing user's information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,blank=True,null=True)
    languages = models.ManyToManyField(Languages, blank=True)
    matches = models.ManyToManyField(MetaProfile,blank=True)

    def __str__(self):
        return self.user.username
