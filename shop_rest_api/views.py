# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from shop_rest_api.serializers import *


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = FileListSerializer
    queryset = Image.objects.all()
    parser_classes = (MultiPartParser, FormParser,)

    def list(self, request):
        queryset = Image.objects.all()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Image.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)


class ProductionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionSerializer
    queryset = Production.objects.all()


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
                dict(login=True, uid=user.id, username=user.username,
                     address=user.profile.address, phone=user.profile.phone,
                     is_business=user.profile.is_business,
                     is_customer=user.profile.is_customer,
                     detail='User is valid, active and authenticated'))
        else:
            return JsonResponse(dict(login=False, detail='The password is valid, but the account has been disabled!'))
    else:
        return JsonResponse(dict(login=False, detail='The username and password were incorrect.'))
