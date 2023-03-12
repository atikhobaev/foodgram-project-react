from django.contrib import admin

from .models import (Recipe, RecipeIncludeIngredients,
                     RecipeFavorite, RecipeInShoppingCart)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
        'cooking_time',
        'pub_date',
        'image',)
    list_filter = (
        'name',
        'author',
        'tags')
    inline = (RecipeIngredientInline, )
    readonly_fields = ('favorite_count', 'pub_date')
    search_fields = ('name',)

    @admin.display(description='добавлен в избранное')
    def favorite_count(self, recipe):
        return recipe.favorite_recipes.count()


@admin.register(RecipeIncludeIngredients)
class RecipeIncludeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount')
    search_fields = ('recipe',)


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user',)


@admin.register(RecipeInShoppingCart)
class RecipeInShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
