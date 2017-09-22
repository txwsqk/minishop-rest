# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from shop_rest_api.models import *


class ProductionInline(admin.TabularInline):
    model = Production


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        ProductionInline,
    ]
    list_display = ('id', 'user', 'phone', 'address', 'is_business', 'is_customer')


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instruction', 'image', 'business', 'recommend_times', 'status')


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'production', 'content', 'user', 'create_time', 'extra')

