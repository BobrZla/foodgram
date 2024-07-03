from django.db import models
from users.models import User
from .validators import validate_time_cooking, validate_amount_ingredients


class Tag(models.Model):
    """Теги рецептов."""
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
        format='hex',
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
    )
    REQUIRED_FIELDS = ('name', 'color', 'slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиенты."""
    name = models.CharField(
        'Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )
    REQUIRED_FIELDS = ('name', 'measurement_unit')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes_author',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        upload_to='recipes/%Y/%m/%d/',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        'Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    time_cooking = models.PositiveIntegerField(
        'Время приготовления',
        validators=[validate_time_cooking],
    )
    REQUIRED_FIELDS = (
        'author',
        'name',
        'image',
        'text',
        'ingredients',
        'tags',
        'time_cooking',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Ингредиенты рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        'Количество ингредиента',
        validators=[validate_amount_ingredients],
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        ordering = ('id',)
        contraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return self.ingredient.name
