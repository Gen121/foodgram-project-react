from django.core.exceptions import ValidationError

UNCORRECT_NAME = [
    'me',
    'login',
    'username',
]


def validate_username(username):
    if username in UNCORRECT_NAME:
        raise ValidationError(f'{username} - Недоступное имя пользователя.')
