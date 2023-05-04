from django.core.exceptions import ValidationError
from datetime import datetime


def current_year(value):
    if value > datetime.now().year:
        raise ValidationError('Nobody can travel in the future')
    return True
