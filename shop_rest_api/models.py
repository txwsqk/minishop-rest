# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(max_length=50)
    extra = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_business = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


class Production(CommonInfo):
    STATUS = (
        ("online", "online"),
        ("offline", "offline"),
    )

    business = models.ForeignKey(UserProfile, related_name='production')
    instruction = models.CharField(max_length=200)
    image = models.ImageField()
    recommend_times = models.IntegerField(default=3)
    status = models.CharField(choices=STATUS, max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-update_time',)


class Comment(models.Model):
    production = models.ForeignKey(Production, related_name='comment')
    content = models.CharField(max_length=200)
    user = models.ForeignKey(UserProfile)
    create_time = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-create_time',)
