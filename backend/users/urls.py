from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

app_name = 'users'

router = SimpleRouter()

router.register('users', UserViewSet)

djoser = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns = [
    path('', include(djoser)),
    path('', include(router.urls)),
]
