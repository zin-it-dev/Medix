from django.urls import path, include
from rest_framework import routers

from .apiviews import CategoryViewSet, CourseViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
