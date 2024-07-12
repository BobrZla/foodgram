from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


def validate_username(value):
    username_validator = UnicodeUsernameValidator()
    username_validator(value)
    if value.lower() == "me":
        raise ValidationError("Недопустимое значение для username.")
