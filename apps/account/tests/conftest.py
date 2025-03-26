import pytest
import factory
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Prevents unnecessary save()

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Ensures the manager's create_user method is used."""
        password = kwargs.pop("password", "defaultpassword")
        return model_class.objects.create_user(password=password, *args, **kwargs)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Prevents unnecessary save()

    email = 'admin@gmail.com'
    password = factory.PostGenerationMethodCall("set_password", "1234")
    is_staff = True
    is_superuser = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Ensures create_superuser() is used, triggering validation."""
        password = kwargs.pop("password", "adminpassword")
        return model_class.objects.create_superuser(password=password, *args, **kwargs)


@pytest.fixture
def api_client() -> APIClient:
    """Returns an APIClient instance."""
    return APIClient()


@pytest.fixture
def test_user(db) -> User:
    """Creates and returns a regular user."""
    return UserFactory(password="userpassword")


@pytest.fixture
def admin_user(db) -> User:
    """Creates and returns a superuser."""
    return SuperUserFactory(password="adminpassword")
