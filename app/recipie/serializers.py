from rest_framework import serializers

from core.models import Tag, Ingredient, Recipie



class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag obects"""

    
    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient obects"""

    
    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)

class RecipieSerializer(serializers.ModelSerializer):
    """Serializer for Recipie obects"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipie
        fields = ('id','title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link')
        read_only_fields = ('id',)
