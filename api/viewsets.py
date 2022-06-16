import uuid
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions
from .serializers import AuthorSerializer, ArticleSerializer, UserRegisterSerializer, LoggedArticleSerializer, \
    LoggedOutArticleSerializer
from api import models
from django.views import generic
from django_filters.rest_framework import DjangoFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import AuthorDocument, ArticleDocument
from .serializers import AuthorSerializer, ArticleSerializer
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, CompoundSearchFilterBackend


class IndexView(generic.ListView):
    template_name = 'index.html'


class Register(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'RequestId': str(uuid.uuid4()),
                'Message': 'User has been created',
                'User': serializer.data}, status=status.HTTP_201_CREATED,
            )
        return Response()


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer
    queryset = models.Author.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Article.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'summary', 'body']

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return LoggedArticleSerializer
        else:
            return LoggedOutArticleSerializer

class LoggedOutViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = models.Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fileds = ['category', 'title', 'summary']

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return LoggedArticleSerializer
        else:
            return LoggedOutArticleSerializer





# Elastic searh views


class AuthorDocumentView(DocumentViewSet):
    document = AuthorDocument
    serializer_class = AuthorSerializer

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend
    ]

    search_fields= ('name', 'picture')
    multi_match_search_fields= ('name', 'picture')
    filter_fields = {
        'name': 'name',
        'picture': 'picture'

    }


class ArticleDocumentView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleSerializer

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend
    ]

    search_fields= ("id", "author_id", "author", "category", "title", "summary", "firstParagraph", "body")
    multi_match_search_fields = ("id", "author_id", "author", "category", "title", "summary", "firstParagraph", "body")
    filter_fields = {
        "id": "id",
        "author_id": "author_id",
        "author": "author",
        "category": "category",
        "title": "title",
        "summary": "summary",
        "firstParagraph": "firstParagraph",
        "body": "body"
    }
