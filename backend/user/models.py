import os

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserPerferences(models.Model):
    # this model will store the perferences of spending of the user which can be used in display and for llm, stored in list of dictionaries
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    phone = models.IntegerField('Phone Number', blank=True, null=True)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.name, self.user.username)