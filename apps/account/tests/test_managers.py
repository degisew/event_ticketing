import pytest
from django.contrib.auth import get_user_model
from conftest import SuperUserFactory, UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_creation(test_user) -> None:
    with pytest.raises(ValueError, match="The Email must be set"):
        UserFactory(email="", password="userpassword")

    assert '@' in test_user.email  # Ensure it's an email
    assert not test_user.is_staff
    assert not test_user.is_superuser
    assert test_user.check_password("userpassword")   # Ensure password is hashed


@pytest.mark.django_db
def test_super_user_creation(admin_user) -> None:
    assert '@' in admin_user.email  # Ensure it's an email
    assert admin_user.check_password("adminpassword")  # Ensure password is hashed
    assert admin_user.is_staff
    assert admin_user.is_superuser

    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        SuperUserFactory(password="adminpassword", is_staff=False)

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        SuperUserFactory(password="adminpassword", is_superuser=False)
