from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from apps.account.services import UserProfileService
from apps.account.models import Role
from apps.account.serializers import (
    PasswordChangeSerializer,
    RoleSerializer,
    UserProfileResponseSerializer,
    UserSerializer,
    UserProfileSerializer,
)


User = get_user_model()


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.select_related("role", "state").all()

    @extend_schema(
        request=UserProfileSerializer, responses=UserProfileResponseSerializer
    )
    @action(methods=["get", "post", "patch"], detail=False, url_path="me")
    def profile(self, request, *args, **kwargs):
        user = request.user

        if request.method == "GET":
            profile = UserProfileService.get_user_profile(user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = UserProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            user.is_profile_set = True
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PATCH":
            profile = UserProfileService.get_user_profile(user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Generate a new JWT token
        refresh = RefreshToken.for_user(request.user)
        return Response(
            {
                "message": "Password changed successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
