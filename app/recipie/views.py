from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipie

from recipie import serializers


class BaseRecipieAttrViewSet(viewsets.GenericViewSet, 
        mixins.ListModelMixin, mixins.CreateModelMixin):
      """ test """
      authentication_classes = (TokenAuthentication,)
      permission_classes = (IsAuthenticated,)

      def get_queryset(self):
          """ """
          return self.queryset.filter(user=self.request.user).order_by('-name')
    
      def perform_create(self, serializer):
            serializer.save(user=self.request.user)
    



class TagViewSet(BaseRecipieAttrViewSet):
    """Manage tags in db"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipieAttrViewSet):
    """Manage Ingredients in db"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

class RecipieViewSet(viewsets.ModelViewSet):
    """Manage Ingredients in db"""
    queryset = Recipie.objects.all()
    serializer_class = serializers.RecipieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """ """
        return self.queryset.filter(user=self.request.user)
