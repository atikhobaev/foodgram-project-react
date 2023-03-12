from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Recipe,
                            RecipeFavorite,
                            RecipeIncludeIngredients,
                            RecipeInShoppingCart)
from users.serializers import UserRecipeSerializer

from .filters import RecipeFilter
from .paginators import PageLimitPagination
from .serializers import RecipeSerializer, RecipeSerializerCreateUpdate


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeSerializerCreateUpdate
        return RecipeSerializer

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if RecipeFavorite.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Рецепт уже есть в избранном')
        RecipeFavorite.objects.create(user=user, recipe=recipe)
        serializer = UserRecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not RecipeFavorite.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Рецепта нет в избранном')
        favorite = get_object_or_404(RecipeFavorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if RecipeInShoppingCart.objects.filter(user=user, recipe=recipe
                                               ).exists():
            raise exceptions.ValidationError(
                'Рецепт уже есть в корзине покупок'
            )
        RecipeInShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = UserRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not RecipeInShoppingCart.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Рецепта нет в корзине покупок')
        shopping_cart = get_object_or_404(
            RecipeInShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIncludeIngredients.objects.filter(
            recipe__shopping_cart_recipes__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('amount'))
        result = (
            'Список покупок:\n\nИнгридиент - кол-во (ед изм)\n')
        result += '\n'.join([
            f'{ingredient["ingredient__name"]} - {ingredient["total"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            for ingredient in ingredients
        ])
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={"shopping_cart.txt"}')
        return response
