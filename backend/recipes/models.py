from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser
from .constant import (
    LEN_TAG_NAME,
    LEN_TAG_SLUG,
    LEN_INGREDIENT_NAME,
    LEN_INGREDIENT_MEASUREMENT_UNIT,
    LEN_RECIPE_NAME,
    MIN_COOKING_TIME,
    MAX_COOKING_TIME,
    MIN_AMOUNT,
    MAX_AMOUNT,
)


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=LEN_TAG_NAME,
        unique=True,
        help_text="Название тега, не более 32 символов.",
    )
    slug = models.SlugField(
        "Слаг тега",
        max_length=LEN_TAG_SLUG,
        unique=True,
        help_text="Слаг тега, не более 32 символов.",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиенты."""

    name = models.CharField(
        "Название ингредиента",
        max_length=LEN_INGREDIENT_NAME,
        unique=True,
        help_text="Название ингредиента, не более 200 символов.",
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=LEN_INGREDIENT_MEASUREMENT_UNIT,
        help_text="Единица измерения, не более 200 символов.",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        "Название рецепта",
        max_length=LEN_RECIPE_NAME,
        help_text="Название рецепта, не более 256 символов.",
    )
    image = models.ImageField(
        "Картинка",
        upload_to="api/recipes/",
        help_text="Картинка рецепта.",
    )
    text = models.TextField(
        "Описание рецепта",
        help_text="Описание рецепта.",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты",
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        related_name="recipes",
        blank=True,
    )
    cooking_time = models.PositiveIntegerField(
        "Время приготовления в минутах",
        validators=[
            MinValueValidator(MIN_COOKING_TIME),
            MaxValueValidator(MAX_COOKING_TIME)
        ],
        help_text="Время приготовления в минутах от 1 до 32000.",
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Список покупок."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_shopping_cart",
        verbose_name="Рецепт",
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_shopping_cart",
            )
        ]

    def __str__(self):
        return (
            f"Рецепт {self.recipe} в списке покупок пользователя {self.user}"
        )


class Favourites(models.Model):
    """Избранное."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="favourites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_favourites",
        verbose_name="Рецепт",
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favourites",
            )
        ]

    def __str__(self):
        return f"Рецепт {self.recipe} в избранном пользователя {self.user}"


class RecipeIngredient(models.Model):
    """Ингредиенты рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="RecipeIngredient",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="RecipeIngredient",
        verbose_name="Ингредиент из рецепта",
    )
    amount = models.PositiveIntegerField(
        "Количество",
        validators=[
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        ],
        help_text="Количество ингредиента в рецепте от 1 до 32000.",
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return f"Ингредиент {self.ingredient} в рецепте {self.recipe}"
