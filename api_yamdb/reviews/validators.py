from django.core.exceptions import ValidationError


def validate_rating(value):
    if value < 1 or value > 10:
        raise ValidationError('Your score must be between 1 and 10 inclusive')
    return True
