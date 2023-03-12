from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet

app_name = 'recipes'

router = SimpleRouter()

router.register('recipes', RecipeViewSet)

urlpatterns = [path('', include(router.urls))]
