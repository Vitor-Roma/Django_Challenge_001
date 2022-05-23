import uuid
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions
from .serializers import AuthorSerializer, ArticleSerializer, UserRegisterSerializer, LoggedArticleSerializer, \
    LoggedOutArticleSerializer
from api import models
from django.views import generic
from django_filters.rest_framework import DjangoFilterBackend


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
    # filterset_fields = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Article.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'summary', 'body']

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return LoggedArticleSerializer
        else:
            return LoggedOutArticleSerializer

class LoggedOutViewSet(viewsets.ModelViewSet):
    serializer_class = LoggedOutArticleSerializer
    queryset = models.Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fileds = ['category', 'title', 'summary']

