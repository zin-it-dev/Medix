from rest_framework import viewsets, generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from .models import Category, Course
from .sec_models import User
from .serializers import CategorySerializer, CourseSerializer, UserSerializer
from .paginators import TinyResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True).all().order_by('-created_on')
    serializer_class = CategorySerializer
    pagination_class = TinyResultsSetPagination
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active=True).all().order_by('-created_on')
    serializer_class = CourseSerializer
    pagination_class = TinyResultsSetPagination
    

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.filter(is_active=True).all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = None