from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from apps.core.validators import (
    validate_email,
    validate_password
)
from apps.account.enums import AccountState, RoleCode
from apps.account.models import Role, UserProfile
from apps.core.models import DataLookup
from apps.core.serializers import DataLookupSerializer


User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "code", "created_at", "updated_at"]


class UserResponseSerializer(serializers.ModelSerializer):
    state = DataLookupSerializer()
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "role",
            "state",
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password"
        ]

    def validate(self, attrs):
        validate_email(attrs.get("email"))
        validate_password(attrs.get("password"))

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords did not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        try:
            # Fetch the account state
            account_state = DataLookup.objects.get(
                type=AccountState.TYPE.value,
                value=AccountState.ACTIVE.value
            )
            role = Role.objects.get(
                code=RoleCode.USER.value
            )
            # Create the user
            user = super().create(validated_data)
            user.state = account_state
            user.role = role
            user.password = make_password(password)
            user.save()
            return user
        except DataLookup.DoesNotExist:
            raise serializers.ValidationError("Active state not found in DataLookup.")

    def to_representation(self, instance):
        return UserResponseSerializer(
            instance, self.context
        ).to_representation(instance)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        validate_password(data["new_password"])
        if data["new_password"] == data["old_password"]:
            raise serializers.ValidationError(
                "You can't use the old password. please choose a new one."
            )
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "address",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)

    def to_representation(self, instance):
        return UserProfileResponseSerializer(
            instance, self.context
        ).to_representation(instance)


class UserProfileResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "address",
            "user",
            "created_at",
            "updated_at"
        ]
