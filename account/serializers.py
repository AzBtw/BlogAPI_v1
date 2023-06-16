from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from posts.serializers import PostListSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8, write_only=True, required=True)
    password_confirmation = serializers.CharField(
        min_length=8, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')

    def validate(self, attrs):
        # print(attrs)
        password2 = attrs.pop('password_confirmation')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Passwords don\'t match')
        validate_password(attrs['password'])
        return attrs

    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError('Name must be capitalized')
        return value

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    # posts = PostListSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

    # def to_representation(self, instance):
    #     repr = super().to_representation(instance)
    #     repr['post_count'] = instance.posts.count()
    #     return repr


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
