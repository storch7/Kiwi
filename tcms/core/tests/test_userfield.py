import pytest
from django.core.exceptions import ValidationError
from tcms.core.forms.fields import UserField
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create(username="joao", email="joao@example.com")

@pytest.fixture
def field_required():
    return UserField(required=True)

@pytest.fixture
def field_optional():
    return UserField(required=False)

# CT1
def test_clean_none_required(field_required):
    with pytest.raises(ValidationError, match="required"):
        field_required.clean(None)

# CT2
def test_clean_empty_optional(field_optional):
    assert field_optional.clean("") is None

# CT3
def test_clean_int_invalid(field_required):
    with pytest.raises(ValidationError, match="Unknown user_id"):
        field_required.clean(9999)

# CT4
def test_clean_str_digit_invalid(field_required):
    with pytest.raises(ValidationError, match="Unknown user_id"):
        field_required.clean("8888")

# CT5
def test_clean_invalid_email(field_required):
    with pytest.raises(ValidationError, match="Unknown user"):
        field_required.clean("notfound@example.com")

# CT6
def test_clean_valid_id(field_required, user):
    assert field_required.clean(user.pk) == user

# CT7
def test_clean_valid_username(field_required, user):
    assert field_required.clean("joao") == user
