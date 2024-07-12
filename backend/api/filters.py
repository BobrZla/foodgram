from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Tag, Recipe
from users.models import CustomUser


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(
        field_name="author", queryset=CustomUser.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method="get_is_favorited",
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart",
    )

    class Meta:
        model = Recipe
        fields = ("tags",)

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(in_favourites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(in_shopping_cart__user=user)
        return queryset
