from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from ingredients.models import Ingredient
from rest_framework import exceptions, serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer

from .models import Recipe, RecipeIncludeIngredients


class RecipeAddIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(1, message='Минимум один ингридиент'),
        )
    )

    class Meta:
        model = RecipeIncludeIngredients
        fields = ('id', 'amount')


class RecipeIncludeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIncludeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIncludeIngredients.objects.filter(recipe=obj)
        serializer = RecipeIncludeIngredientsSerializer(ingredients, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        if (
            self.context['request'].user.is_authenticated
            and obj.favorite_recipes.filter(
                    user=self.context['request'].user
                ).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if (self.context['request'].user.is_authenticated
            and obj.shopping_cart_recipes.filter(
                    user=self.context['request'].user
                ).exists()):
            return True
        return False


class RecipeSerializerCreateUpdate(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = RecipeAddIngredientsSerializer(many=True)
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(1, message='Минимум одна минута'),
        )
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError('Минимум один тег')
        return value

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError('Минимум один ингридиент')
        ingredients = [item['id'] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError('Ингридиенты повторяются')
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

            RecipeIncludeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient['amount']
                ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

                RecipeIncludeIngredients.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'amount': amount}
                )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data
