from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import views
from recipes.paginators import PageLimitPagination
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Subscriptions

from .serializers import UserSubscribeSerializer

User = get_user_model()


class UserViewSet(views.UserViewSet):
    pagination_class = PageLimitPagination

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribers__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = UserSubscribeSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['POST'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({'errors': 'Невозможно подписаться на себя'},
                            status=status.HTTP_400_BAD_REQUEST)
        if Subscriptions.objects.filter(user=user, author=author
                                        ).exists():
            return Response({'errors': 'Подписка уже оформлена'},
                            status=status.HTTP_400_BAD_REQUEST)
        Subscriptions.objects.create(user=user, author=author)
        serializer = UserSubscribeSerializer(author,
                                             context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if not Subscriptions.objects.filter(user=user, author=author).exists():
            return Response(
                {'errors': 'Подписки не существует'},
                status=status.HTTP_400_BAD_REQUEST)
        Subscriptions.objects.get(
            user=user,
            author=author
            ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
