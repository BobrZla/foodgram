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
)
from users.models import CustomUser, Follow
from .paginations import CustomPagination
from recipes.models import Recipe, Tag, Ingredient
from .filters import IngredientFilter


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
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
