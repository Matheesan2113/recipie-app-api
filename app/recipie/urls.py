from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipie import views



router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipies', views.RecipieViewSet)

app_name = 'recipie'

urlpatterns = [
    path('', include(router.urls))
]