from django.shortcuts import render
from rest_framework import viewsets
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomUserSerializer, UserAvatarSerializer
from users.models import CustomUser
from .paginations import CustomPagination


class UsersViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        methods=['put', 'delete'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me/avatar'
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
