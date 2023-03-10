from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения ингредиента',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'
