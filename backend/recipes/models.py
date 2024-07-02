from django.db import models
from django.contrib.auth import get_user_model




class Tag(models.Model):
# Название.
# Slug.
    pass

class Ingredient(models.Model):
# Название.
# Slug.
    pass

class Recipe(models.Model):

# Автор публикации (пользователь).
# Название.
# Картинка.
# Текстовое описание.
# Ингредиенты — продукты для приготовления блюда по рецепту. Множественное поле с выбором из предустановленного списка и с указанием количества и единицы измерения.
# Тег. Можно установить несколько тегов на один рецепт.
# Время приготовления в минутах.
    pass


