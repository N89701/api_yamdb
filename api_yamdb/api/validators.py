import string

from django.core.exceptions import ValidationError


def validate_username_is_not_me(value):
    if value == 'me':
        raise ValidationError(
            '"me" - запрещено использовать как имя пользователя'
        )
    return value


def validate_username(value):
    forbidden_symbols = ''
    allowed_letters = string.ascii_letters
    allowed_symbols = '@/./+/-/_'
    allowed_chars = allowed_letters + allowed_symbols
    for char in value:
        if char not in allowed_chars:
            forbidden_symbols += char
    if forbidden_symbols:
        raise ValidationError(f'Некорректный символ для никнейма: '
                              f'{forbidden_symbols} Только буквы, цифры и @/./+/-/_')
    return value
