from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

UNCORRECT_NAME = {
    'me',
    'login',
    'username',
}


def custom_username_validator(username):
    if username in UNCORRECT_NAME:
        raise ValidationError(f'{username} - Недоступное имя пользователя.')


class CustomUsernameValidator(UnicodeUsernameValidator):
    def __call__(self, value):
        custom_username_validator(value)
        return super().__call__(value)
