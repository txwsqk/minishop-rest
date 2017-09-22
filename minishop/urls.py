# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from shop_rest_api.views import *

router = routers.DefaultRouter()
router.register(r'account', UserView)
router.register(r'production', ProductionViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    url(r'^account/login/', login_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
]
