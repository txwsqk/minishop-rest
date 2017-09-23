# -*- coding:utf-8 -*-
from rest_framework import serializers

from shop_rest_api.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('production', 'content', 'user', 'create_time', 'extra')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'production')


class ProductionSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Production
        fields = (
            'id', 'name', 'business', 'instruction', 'image', 'recommend_times',
            'status', 'create_time', 'update_time', 'extra', 'comment'
        )


class FileListSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    image = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=True)
    )

    def create(self, validated_data):
        production = Production.objects.get(pk=self.initial_data.get('production'))
        images = validated_data.pop('image')
        for img in images:
            image = Image.objects.create(image=img, production=production, **validated_data)
        return image


class ProfileSerializer(serializers.ModelSerializer):
    production = ProductionSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'is_business', 'is_customer', 'production')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        UserSerializer.update_or_create_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.get(pk=instance.id)
        user.set_password(validated_data['password'])
        user.save()
        UserSerializer.update_or_create_profile(instance, profile_data)
        return user

    @staticmethod
    def update_or_create_profile(user, profile_data):
        UserProfile.objects.update_or_create(user=user, defaults=profile_data)
