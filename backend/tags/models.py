from django.core import validators
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название тега',
        unique=True,
        db_index=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега в hex формате',
        unique=True,
        validators=[validators.RegexValidator(
            r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
            "Цвет в hex формате, например #1AFFa1",
        )],
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг тега',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name
