from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from users.models import UserProfile
from users.permissions import IsSelfOrReadOnly
from users.serializer import UserRegisterSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        qs = UserProfile.objects.all()
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return qs.none()
        else:
            user: UserProfile
            if user.is_superuser:
                return qs.all()
            else:
                return qs.filter(username=user.username).all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = UserProfile.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        print(serializer.data)
        return Response(serializer.data)

    @action(detail=False)
    def sorted(self, request):
        users = UserProfile.objects.all().order_by('-username')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
