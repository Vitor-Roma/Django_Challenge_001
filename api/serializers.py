from rest_framework import serializers
from api import models
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email already exists'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username already exists'})

        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)
    author_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = models.Article
        fields = ["id", "author_id", "author", "category", "title", "summary", "firstParagraph", "body"]


class LoggedArticleSerializer(ArticleSerializer):
    pass


class LoggedOutArticleSerializer(ArticleSerializer):
    class Meta:
        model = models.Article
        exclude = ('body',)
