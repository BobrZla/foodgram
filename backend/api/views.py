import csv
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .serializers import (
    CustomUserSerializer,
    UserAvatarSerializer,
    FollowSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    ShortRecipeSerializer,
    ShoppingCartSerializer,
)
from users.models import CustomUser, Follow
from .paginations import CustomPagination
from recipes.models import Recipe, Tag, Ingredient, Favourites, ShoppingCart, RecipeIngredient
from .filters import IngredientFilter, RecipeFilter
from foodgram.settings import HOST
from django.db.models import Sum


class UsersViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        methods=['put', 'delete'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me/avatar',
    )
    def avatar(self, request):
        if request.method == 'PUT':
            instance = self.get_instance()
            serializer = UserAvatarSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            instance = self.get_instance()
            instance.avatar = None
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        is_subscribed = Follow.objects.filter(
            user=user, author=author
        ).exists()
        if request.method == 'POST':
            if author == user or is_subscribed:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = FollowSerializer(author, context={'request': request})
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not is_subscribed:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(following__user=user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            paginated_queryset, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me',
    )
    def me(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return RecipeSerializer
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            serializer = FavoriteSerializer(data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if Favourites.objects.filter(user=user, recipe=recipe).exists():
                Favourites.objects.filter(user=user, recipe=recipe).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(data={'errors': 'Этого рецепта нет в избранном.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(data={'errors': 'Этого рецепта нет в списке покупок.'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__in_shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        print(ingredients)

        shopping_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])

        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    @action(
        detail=True,
        methods=['GET'],
        url_path='get-link',
    )
    def get_link(self, request, pk):
        get_object_or_404(Recipe, id=pk)
        return Response({"short-link": f"{HOST}/recipes/{pk}"},
                        status=status.HTTP_200_OK)
