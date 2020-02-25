from django.utils.crypto import get_random_string



def format_phone_number(number):
    if len(number) == 13:
        if number.startswith('234'):
            return number
    elif len(number) == 11:
        if number.startswith('0'):
            return number.replace('0', '234', 1)
    elif len(number) == 10:
        return '234' + number
    return None

def unique_generator(model, field, length=12, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    unique = get_random_string(length=length, allowed_chars=allowed_chars)
    kwargs = {field: unique}
    qs_exists = model.objects.filter(**kwargs).exists()
    if qs_exists:
        return unique_generator(model, field)
    return unique
