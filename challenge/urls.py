from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import viewsets
from api.viewsets import Register
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

route = routers.DefaultRouter()


route.register(r'api/admin/authors', viewsets.AuthorViewSet, basename='Authors')
route.register(r'api/admin/articles', viewsets.ArticleViewSet, basename='Admin/Articles')
route.register(r'api/articles', viewsets.LoggedOutViewSet, basename='Articles')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/sign-up/', Register.as_view(), name='sign-up'),
    path('', include(route.urls)),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
