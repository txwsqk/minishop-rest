# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from shop_rest_api.serializers import *


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionSerializer
    queryset = Production.objects.all()
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(
            business=UserProfile.objects.get(pk=self.request.data.get('business')),
            instruction=self.request.data.get('instruction'),
            image=self.request.data.get('image'),
            recommend_times=self.request.data.get('recommend_times'),
            status=self.request.data.get('status'),
            create_time=self.request.data.get('create_time'),
            update_time=self.request.data.get('update_time'),
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


@csrf_exempt
@require_http_methods('POST')
def login_view(request):
    json_data = json.loads(request.body)
    username = json_data.get('username')
    password = json_data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return JsonResponse(
                dict(login=True, uid=user.id, username=user.username, detail='User is valid, active and authenticated'))
        else:
            return JsonResponse(dict(login=False, detail='The password is valid, but the account has been disabled!'))
    else:
        return JsonResponse(dict(login=False, detail='The username and password were incorrect.'))
