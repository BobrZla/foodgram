from django.core.exceptions import ValidationError


def validate_time_cooking(cooking_time):
    if cooking_time <= 0:
        raise ValidationError(
            'Время приготовления должно быть положительным числом.'
        )
    return cooking_time


def validate_amount_ingredients(ingredients):
    if len(ingredients) == 0:
        raise ValidationError(
            'Рецепт должен содержать хотя бы один ингредиент.'
        )
    return ingredients
